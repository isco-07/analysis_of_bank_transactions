import logging
from typing import Any
import os


logs = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(logs):
    os.mkdir(logs)


def my_logger() -> Any:
    """Функция создает и взвращает logger с хендлерами на запись в файл и форматер вида
    (временная метка, название модуля, уровень серьезности и сообщение, описывающее событие или ошибку)"""
    logger = logging.getLogger("my_log")
    file_handler = logging.FileHandler(f"{logs}/logs.log", "a+", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s %(filename)s %(levelname)s: %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.setLevel(level=logging.INFO)
    return logger
