import json
import re
from datetime import datetime

from src.logger import my_logger


def search_phone_numbers(data: list) -> str:
    """Возвращает JSON со всеми транзакциями, содержащими в описании мобильные номера"""
    if not data:
        my_logger().debug("Нет данных для анализа")

        return "[]"
    else:
        pattern = re.compile(r"(\+7|8).*?(\d{3}).*?(\d{3}).*?(\d{2}).*?(\d{2})")
        transactions = [x for x in data if pattern.search(x["Описание"])]
        tr_info = []
        for tr in transactions:
            date = datetime.strptime(tr["Дата платежа"], "%d.%m.%Y").strftime("%d.%m.%Y")
            info = {
                "date": date,
                "amount": tr["Сумма операции"],
                "category": tr["Категория"],
                "description": tr["Описание"],
            }
            tr_info.append(info)
        json_response = json.dumps(tr_info, ensure_ascii=False, indent=4)

        my_logger().debug("Создан json-ответ с операциями где есть номер телефона в описании")

        return json_response
