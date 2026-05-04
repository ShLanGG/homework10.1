"""Отчёты"""
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from src.decorators import report_to_file
import logging

logger = logging.getLogger(__name__)

@report_to_file()
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """Траты по категории за последние 3 месяца от даты."""
    end = datetime.now() if date is None else datetime.strptime(date, "%Y-%m-%d")
    start = end - pd.DateOffset(months=3)
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True, errors='coerce')
    mask = (transactions['Категория'] == category) & (transactions['Дата операции'] >= start) & (transactions['Дата операции'] <= end)
    return transactions.loc[mask].copy()