import configparser
import os
import time
from logging import getLevelName, _checkLevel, DEBUG
from pathlib import Path


def file_size(file_path: str) -> int:
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return round(file_info.st_size / 1000000)
    return 0


def log_event(level: int, details: str) -> None:
    with open("config.ini") as file:
        config = configparser.RawConfigParser(allow_no_value=True)
        config.read_string(file.read())
        if level < _checkLevel(config.get('logging', 'level')):
            return

    current_log_path = f'logs/{str(time.strftime("%Y%m%d-%H%M%S"))}.log'

    Path("logs").mkdir(exist_ok=True)

    formatted_datetime = str(time.strftime("%Y%m%d-%H%M%S"))

    if file_size(current_log_path) > config.getint('logging', 'maximum-file-size'):
        current_log_path = f'logs/{formatted_datetime}.log'

    log_entry = f'{formatted_datetime} >>> {getLevelName(level)} >>> {details}'

    with open(current_log_path, 'a+') as log_file: log_file.write(f'{log_entry}\n')

    print(log_entry)


def log_event__command_begin(command_name: str) -> None:
    log_event(DEBUG, f'command <{command_name}> has been called, execution has begun')


def log_event__command_end(command_name: str) -> None:
    log_event(DEBUG, f'command <{command_name}> execution has ended')
