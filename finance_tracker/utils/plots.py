import matplotlib
matplotlib.use('Agg')  # для работы без GUI
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pandas as pd

# График доходов/расходов по времени

def plot_income_expense(df):
    if df.empty or 'amount' not in df.columns:
        return None
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    if df['amount'].dropna().empty:
        return None
    df_grouped = df.groupby(['date', 'type'])['amount'].sum().unstack(fill_value=0)
    if df_grouped.empty:
        return None
    plt.figure(figsize=(8, 4))
    df_grouped.plot(ax=plt.gca())
    plt.title('Доходы и расходы по времени')
    plt.xlabel('Дата')
    plt.ylabel('Сумма')
    plt.legend(['Доход', 'Расход'])
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return img_str

# Диаграмма расходов по категориям

def plot_expense_pie(df):
    if df.empty or 'amount' not in df.columns:
        return None
    df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
    df_expense = df[df['type'] == 'expense']
    if df_expense.empty:
        return None
    df_grouped = df_expense.groupby('category__name')['amount'].sum()
    if df_grouped.empty:
        return None
    plt.figure(figsize=(6, 6))
    df_grouped.plot.pie(autopct='%1.1f%%')
    plt.title('Расходы по категориям')
    plt.tight_layout()
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return img_str