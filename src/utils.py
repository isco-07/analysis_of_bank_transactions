import json

import pandas as pd

from src.logger import my_logger


# CONST_URL = 'https://finnhub.io/'
# CONST_KEY = 'cll4fmpr01qhqdq2gri0cll4fmpr01qhqdq2grig'
def read_xls(file_path: str) -> list:
    return pd.read_excel(file_path, index_col=0).to_dict(orient="records")


def read_user_settings(file_path: str) -> dict:
    try:
        with open(file_path, encoding="utf-8") as f:
            json_dict = json.load(f)
        my_logger().debug("Сформирован список словарей с операциями")
        return json_dict
    except FileNotFoundError:
        my_logger().debug("Файл не найден")
        return {}


# s = read_xls("../data/operations.xls")
#
# for i in s:
#     print(i)
