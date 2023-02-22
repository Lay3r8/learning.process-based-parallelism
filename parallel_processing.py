from multiprocessing import Pool, cpu_count
from timeit import timeit
from typing import Final
from alive_progress import alive_bar
from pandas import read_table, DataFrame
from requests import post


LARGE_FILE: Final = "inputs/US_Accidents_Dec21_updated.csv"
BACKEND_URL: Final = "http://localhost:8000/accidents"
CSV_REPORT_PATH: Final = "./outputs/np_report.csv"
GENERATOR_MAX_LINES: Final = 10000
GENERATOR_OUTPUT: Final = "inputs/demo.csv"
CHUNKSIZE: Final = GENERATOR_MAX_LINES / 10


class CsvReport:

    def __init__(self, path) -> None:
        self.headers = ["postgres_id", "accident_id", "description", "latitude", "longitude", "severity", "timestamp", "timezone", "status_code"]
        self.path = path
        self.lines = []
        with open(path, mode="w", encoding="utf-8") as f_out:
            f_out.write(f"{','.join(self.headers)}\n")

    def add_line(self, line: str) -> None:
        self.lines.append(line)

    def save(self, lines=None) -> None:
        with open(self.path, mode="a", encoding="utf-8") as f_out:
            f_out.writelines(lines if lines else self.lines)

    def clear_lines(self) -> None:
        self.lines = []


def process_frame(df: DataFrame) -> str:
    ret = []
    for row in df.itertuples(index=False):
        response = post(BACKEND_URL, data={
            "accident_id": row.ID,
            "severity": row.Severity,
            "timestamp": row.Start_Time,
            "timezone": row.Timezone,
            "latitude": row.Start_Lat,
            "longitude": row.Start_Lng,
            "description": row.Description,
        })
        if response.status_code == 201:
            d = response.json()
            ret.append(f"{d['id']},{d['accident_id']},{d['description']},{d['latitude']},{d['longitude']},{d['severity']},{d['timestamp']},{d['timezone']},{response.status_code}\n")
        else:
            ret.append(f"ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,ERROR,{response.status_code}\n")
    return ret


class Main():

    def __init__(self) -> None:
        file = GENERATOR_OUTPUT
        self.reader = read_table(
            file,
            header=0,
            delimiter=',',
            usecols=["ID", "Severity", "Start_Time", "Start_Lat", "Start_Lng", "Description", "Timezone"],
            chunksize=CHUNKSIZE
        )
        self.csv_report = CsvReport(CSV_REPORT_PATH)
        self.num_lines = int(sum(1 for _ in open(file)) / CHUNKSIZE)
        self.count = 0
        self.num_workers = cpu_count() * 2
        self.pool = Pool(self.num_workers)
        self.async_results = []
        self.bar = None

    def on_result_callback(self, csv_lines) -> None:
        print("Got lines!")
        self.bar()
        self.csv_report.save(csv_lines)

    def start(self) -> None:
        print(f"Loading tasks of {self.num_workers} workers...")
        with alive_bar(self.num_lines) as bar:
            for df in self.reader:
                results = self.pool.apply_async(process_frame,[df], callback=self.on_result_callback)
                bar()

        print("Tasks loaded! Waiting for workers to finish...")
        with alive_bar(self.num_lines) as bar:
            self.bar = bar
            results.wait()
        print(f"Done!")


if __name__ == '__main__':
    main = Main()
    print(f"Total time in seconds: {timeit(main.start, number=1)}")
