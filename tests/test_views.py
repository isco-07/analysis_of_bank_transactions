from datetime import datetime
from unittest.mock import patch
import pytest

from src.views import (
    card_info,
    greeting,
    # json_answer,
    # currencies_conv,
    trans_of_period,
    #     stocks_conv,
    top_five_transactions,
)


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (datetime(2023, 11, 27, 2, 15, 00, 65651), "Доброй ночи"),
        (datetime(2023, 11, 27, 8, 15, 00, 65651), "Доброе утро"),
        (datetime(2023, 11, 27, 15, 15, 00, 65651), "Добрый день"),
        (datetime(2023, 11, 27, 21, 15, 00, 65651), "Добрый вечер"),
    ],
)
@patch("src.views.datetime")
def test_greeting(mock_datetime, data, expected_result):
    mock_datetime.now.return_value = data
    assert greeting() == expected_result


def test_trans_of_period(tr_list) -> None:
    assert [x["Дата платежа"] for x in trans_of_period(tr_list, "22.09.2019")] == ["21.09.2019"]


def test_card_info(tr_list):
    dict_1 = {"last_digits": "7197", "total_spent": 2107.0, "cashback": 0}
    dict_2 = {"last_digits": "4556", "total_spent": 342.86, "cashback": 0}
    result = card_info(tr_list, [])
    assert dict_1 in result
    assert dict_2 in result


def test_top_five_transactions(tr_list):
    assert top_five_transactions(tr_list) == [
        {
            "date": "21.09.2019",
            "amount": 54871.96,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {
            "date": "21.09.2019",
            "amount": 54871.96,
            "category": "Переводы",
            "description": "Перевод Кредитная карта. ТП 10.2 RUR",
        },
        {"date": "23.09.2019", "amount": 3000.0, "category": "Наличные", "description": "Снятие в банкомате Сбербанк"},
        {"date": "22.09.2019", "amount": 850.0, "category": "Ж/д билеты", "description": "Аэроэкспресс"},
        {"date": "21.09.2019", "amount": 500.0, "category": "Переводы", "description": "Перевод между счетами"},
    ]
