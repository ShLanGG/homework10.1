import pandas as pd
from src.reports import spending_by_category

def test_spending_by_category():
    df = pd.DataFrame({
        "Дата операции": ["01.03.2023", "15.04.2023", "10.05.2023"],
        "Категория": ["Еда", "Еда", "Транспорт"],
        "Сумма операции": [100, 200, 50]
    })
    result = spending_by_category(df, "Еда", "2023-05-20")
    assert len(result) == 2
    assert result["Сумма операции"].sum() == 300