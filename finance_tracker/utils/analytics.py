import pandas as pd
import numpy as np
from core.models import Transaction

def get_transactions_df(user, date_from=None, date_to=None, type=None):
    qs = Transaction.objects.filter(user=user)
    if date_from:
        qs = qs.filter(date__gte=date_from)
    if date_to:
        qs = qs.filter(date__lte=date_to)
    if type:
        qs = qs.filter(type=type)
    # Можно добавить фильтр по категории, если нужно

    df = pd.DataFrame(list(qs.values('date', 'amount', 'type', 'category__name')))
    if df.empty:
        return df
    if not df.empty:
        df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'])
    return df

def detect_anomalies(df):
    # Пример: если по какой-то категории траты за месяц выросли >50% по сравнению с прошлым месяцем
    df_exp = df[df['type'] == 'expense']
    if df_exp.empty:
        return []
    df_exp['month'] = df_exp['date'].dt.to_period('M')
    grouped = df_exp.groupby(['month', 'category__name'])['amount'].sum().unstack(fill_value=0)
    if len(grouped) < 2:
        return []
    last, prev = grouped.iloc[-1], grouped.iloc[-2]
    anomalies = []
    for cat in grouped.columns:
        if prev[cat] > 0 and (last[cat] - prev[cat]) / prev[cat] > 0.5:
            anomalies.append(
                f"В категории '{cat}' расходы выросли более чем на 50% по сравнению с прошлым месяцем!"
            )
    return anomalies

def generate_advice(df):
    # Пример: если категория "Еда" > 30% всех расходов
    advices = []
    df_exp = df[df['type'] == 'expense']
    if df_exp.empty:
        return []
    total = df_exp['amount'].sum()
    cats = df_exp.groupby('category__name')['amount'].sum()
    for cat, amount in cats.items():
        if amount / total > 0.3:
            advices.append(
                f"Вы тратите на '{cat}' более 30% всех расходов. Подумайте, как можно сэкономить."
            )
    return advices

def calculate_stats(df):
    result = {}
    if df.empty:
        result['total_income'] = 0
        result['total_expense'] = 0
        result['balance'] = 0
        return result
    result['total_income'] = df[df['type'] == 'income']['amount'].sum()
    result['total_expense'] = df[df['type'] == 'expense']['amount'].sum()
    result['balance'] = result['total_income'] - result['total_expense']
    return result