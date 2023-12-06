import json
from datetime import datetime
from typing import Any

import requests

from src.logger import my_logger
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")


def greeting() -> str:
    """Возвращает собщение приветствия с соответсвием текущему времени суток"""
    time_now = datetime.now()
    if 5 <= time_now.hour < 12:
        greet = "Доброе утро"
    elif 12 <= time_now.hour < 17:
        greet = "Добрый день"
    elif 17 <= time_now.hour < 22:
        greet = "Добрый вечер"
    else:
        greet = "Доброй ночи"
    my_logger().info(f"Приветствие: {greet}")
    return greet


def trans_of_period(data: list, date_time: str) -> list:
    """Возвращает транзакции за период с начала месяца переданной даты в функцию до переданной даты"""
    day_in_month = datetime.strptime(date_time[:10], "%d.%m.%Y").date()
    first_day_im_month = day_in_month.replace(day=1)
    period_of_days = (day_in_month - first_day_im_month).days
    transactions_of_period = [
        i
        for i in data
        if isinstance(i["Дата платежа"], str)
        and 0 < (day_in_month - datetime.strptime(i["Дата платежа"], "%d.%m.%Y").date()).days <= period_of_days
        and i["Статус"] == "OK"
        and str(i["Номер карты"]) != "nan"
    ]
    my_logger().info("Транзакции за определенный период с начала месяца до дня переданной даты записаны успешно")
    return transactions_of_period


def card_info(period_list: list, rates: list) -> list:
    """Возвращает информацию по картам за переданный период"""
    cards_transactions = []
    cards = sorted(set(i["Номер карты"] for i in period_list))
    for card in cards:
        card_trans = [i for i in period_list if i["Номер карты"] == card]
        spending = 0
        abs(sum(i["Сумма платежа"] if str(i["Сумма платежа"]) != "nan" else 0 for i in card_trans))
        for i in card_trans:
            if i["Валюта операции"] == "RUB":
                spending += i["Сумма платежа"]
            else:
                if rates:
                    for currency in rates:
                        if (i["Сумма платежа"] != "nan") and (i["Валюта операции"] == currency["currency"]):
                            i["Сумма платежа"] = i["Сумма платежа"] * currency["currency"]
                            spending += i["Сумма платежа"]
                            break
                    else:
                        spending += 0
                else:
                    spending += 0
        cashback = sum(i["Кэшбэк"] if str(i["Кэшбэк"]) != "nan" else 0 for i in card_trans)
        cards_transactions.append(
            {"last_digits": card[1:], "total_spent": round(abs(spending), 2), "cashback": cashback}
        )
    my_logger().info("Записана информация по картам")
    return cards_transactions


def top_five_transactions(period: list) -> list:
    """Возвращает топ 5 транзакций за переданный период"""
    five_trans = []
    count = 1
    for trans in sorted(period, key=lambda x: abs(x["Сумма операции"]), reverse=True):
        five_trans.append(
            {
                "date": trans["Дата платежа"],
                "amount": abs(trans["Сумма операции"]),
                "category": trans["Категория"],
                "description": trans["Описание"],
            }
        )
        count += 1
        if count > 5:
            break
    my_logger().info("Записан топ транзакций за определенный период")
    return five_trans


def stocks_conv(settings: list) -> list:
    """Возвращает цены акций с помощью стороннего сервиса через api"""
    stock_prices = []
    if API_KEY:
        for stock in settings:
            url = f"https://finnhub.io/api/v1/quote?symbol={stock}&token={API_KEY}"
            stock_price = requests.get(url).json()["c"]
            stock_prices.append({"stock": stock, "price": round(stock_price, 2)})
        my_logger().info("Добавлен список цен на акции")
        return stock_prices
    else:
        my_logger().warning("Нет API ключа")
        return []


def currencies_conv(settings: list) -> list:
    """Возвращает курсы валют переданого списка"""
    currency_rates = []
    for currency in settings:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        rate = requests.get(url).json()["Valute"][currency]["Value"]
        currency_rates.append({"currency": currency, "rate": round(rate, 2)})
    my_logger().info("Добавлен список по курсу валют")
    return currency_rates


def json_answer(read_xls_list: list, read_user_settings_dict: dict, date: str) -> Any:
    """Возвращает словарь и информацие по картам, топ 5 транзакций за период с начала месяца до текущей даты переданной
    в функцию, курсы валют и цены акций"""
    greet = greeting()
    period_trans = trans_of_period(read_xls_list, date)
    currencies = currencies_conv(read_user_settings_dict["user_currencies"])
    stocks = stocks_conv(read_user_settings_dict["user_stocks"])
    cards_info_list = card_info(period_trans, currencies)
    top_five_trans = top_five_transactions(period_trans)
    response = {
        "greeting": greet,
        "cards": cards_info_list,
        "top_transactions": top_five_trans,
        "currency_rates": currencies,
        "stock_prices": stocks,
    }
    response_json = json.dumps(response, ensure_ascii=False, indent=4)
    my_logger().info("Информация успершно обработа и создана в виде JSON")
    return response_json
