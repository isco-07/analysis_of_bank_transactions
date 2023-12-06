from src.reports import spending_by_category


def test_spending_by_category(tr_list):
    result = spending_by_category(tr_list, "Переводы").to_dict(orient="records")
    assert [x["Категория"] for x in result] == []


def test_spending_by_category_with_date(tr_list):
    result = spending_by_category(tr_list, "Переводы", "21.09.2019").to_dict(orient="records")
    assert [x["Категория"] for x in result] == ["Переводы", "Переводы", "Переводы", "Переводы"]
