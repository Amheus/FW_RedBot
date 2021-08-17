
import os
import time
from pathlib import Path

CURRENT_LOG_PATH = f'logs/{str(time.strftime("%Y%m%d-%H%M%S"))}.log'
MAX_SIZE = 500  # max size of log files before a new one is created, in MB


def convert_bytes_to_mb( num):
    mb = num / 1000000
    return mb


def file_size(filePath):
    if os.path.isfile(filePath):
        fileInfo = os.stat(filePath)
        return convert_bytes_to_mb(fileInfo.st_size)
    return 0


def log_event(txt: str):
    global CURRENT_LOG_PATH
    global MAX_SIZE

    Path("logs").mkdir(exist_ok=True)

    formatted_datetime = str(time.strftime("%Y%m%d-%H%M%S"))

    if file_size(CURRENT_LOG_PATH) > MAX_SIZE:
        CURRENT_LOG_PATH = f'logs/{formatted_datetime}.log'

    log_entry = f'{formatted_datetime} >>> {txt}'

    with open(CURRENT_LOG_PATH, 'a+') as log_file: log_file.write(f'{log_entry}\n')

    print(log_entry)
