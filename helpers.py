import configparser
import os
import time
from logging import getLevelName, _checkLevel
from pathlib import Path




def file_size(file_path):
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size / 1000000
    return 0


def log_event(event_level: int, event_details: str):
    with open("config.ini") as file:
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_string(file.read())
        if event_level < _checkLevel(config.get('logging', 'level')):
            return

    current_log_path = f'logs/{str(time.strftime("%Y%m%d-%H%M%S"))}.log'

    Path("logs").mkdir(exist_ok=True)

    formatted_datetime = str(time.strftime("%Y%m%d-%H%M%S"))

    if file_size(current_log_path) > config.getint('logging', 'maximum-file-size'):
        current_log_path = f'logs/{formatted_datetime}.log'

    log_entry = f'{formatted_datetime} >>> {getLevelName(event_level)} >>> {event_details}'

    with open(current_log_path, 'a+') as log_file: log_file.write(f'{log_entry}\n')

    print(log_entry)
