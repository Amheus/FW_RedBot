import configparser
import os
import time
from logging import getLevelName, _checkLevel
from pathlib import Path

CURRENT_LOG_PATH = f'logs/{str(time.strftime("%Y%m%d-%H%M%S"))}.log'


def convert_bytes_to_mb( num):
    mb = num / 1000000
    return mb


def file_size(filePath):
    if os.path.isfile(filePath):
        fileInfo = os.stat(filePath)
        return convert_bytes_to_mb(fileInfo.st_size)
    return 0


def log_event(event_type: int, event_details: str):
    with open("config.ini") as file:
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_string(file.read())
        if event_type < _checkLevel(config.get('logging', 'level')):
            return

    global CURRENT_LOG_PATH

    Path("logs").mkdir(exist_ok=True)

    formatted_datetime = str(time.strftime("%Y%m%d-%H%M%S"))

    if file_size(CURRENT_LOG_PATH) > config.getint('logging', 'maximum-file-size'):
        CURRENT_LOG_PATH = f'logs/{formatted_datetime}.log'

    log_entry = f'{formatted_datetime} >>> {getLevelName(event_type)} >>> {event_details}'

    with open(CURRENT_LOG_PATH, 'a+') as log_file: log_file.write(f'{log_entry}\n')

    print(log_entry)
