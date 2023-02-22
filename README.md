# Processed based parallelism - a practical example
This repo shows how to use parallelism to speed-up I/O operations when processing large datasets

## Setup
```bash
# Install the Python packages
pyenv virtualenv 3.11.0 parallel-processing-large-file
pyenv activate parallel-processing-large-file
pip install -r requirements.txt

# Start the containers
docker-compose up -d

# Get them rights straight
chmod +x api/start.sh
```

## Usage
```bash
cd api
./start.sh

# Now you can test both types of processing
python normal_processing.py
python parallel_processing.py
```

## Debug
Open the project with VSCode, put some breakpoints and launch the API with the provided debug configuration.

## Going further
* Want to test on bigger dataset? Be my guest: [click here](https://web.archive.org/web/20230124193915/https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents)
* Replace the ASGI server by a classic WSGI one to check if there's a difference. You'll also need to modify the Falcon app in api/app.py
