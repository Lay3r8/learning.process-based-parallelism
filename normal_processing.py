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


def main():
    file = GENERATOR_OUTPUT
    reader = read_table(
        file,
        header=0,
        delimiter=',',
        usecols=["ID", "Severity", "Start_Time", "Start_Lat", "Start_Lng", "Description", "Timezone"],
        chunksize=CHUNKSIZE
    )
    csv_report = CsvReport(CSV_REPORT_PATH)
    num_lines = int(sum(1 for _ in open(file)) / CHUNKSIZE)

    with alive_bar(num_lines) as bar:
        for df in reader:
            csv_report.save(process_frame(df))
            csv_report.clear_lines()
            bar()


def generate_smaller_input_csv() -> None:
    print(f"Generating {GENERATOR_MAX_LINES} lines...")
    with open(LARGE_FILE, "r") as f_in, open(GENERATOR_OUTPUT, "w", encoding="utf-8") as f_out:
        with alive_bar(GENERATOR_MAX_LINES) as bar:
            for _ in range(0, GENERATOR_MAX_LINES):
                f_out.write(f_in.readline())
                bar()
    print("Done!")


if __name__ == '__main__':
    print(f"Total time in seconds: {timeit(main, number=1)}")
    # generate_smaller_input_csv()
