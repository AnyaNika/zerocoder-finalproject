from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Transaction, Category, TelegramProfile
from .forms import TransactionForm, CategoryForm, TelegramProfileForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from utils.analytics import (get_transactions_df, calculate_stats,
                             detect_anomalies, generate_advice, category_report)
from utils.plots import plot_income_expense, plot_expense_pie
from datetime import date, timedelta

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    categories = Category.objects.filter(user=request.user)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    category = request.GET.get('category')

    if date_from:
        transactions = transactions.filter(date__gte=date_from)
    if date_to:
        transactions = transactions.filter(date__lte=date_to)
    if category:
        transactions = transactions.filter(category_id=category)

    return render(request, "core/transaction_list.html", {
        "transactions": transactions,
        "categories": categories
    })

@login_required
def my_categories(request):
    categories = Category.objects.filter(user=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("my_categories")
    else:
        form = CategoryForm()

    return render(request, "core/my_categories.html", {
        "categories": categories,
        "form": form
    })

@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST, user=request.user)  # <-- передаём user
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(user=request.user)  # <-- и здесь тоже
    return render(request, "core/add_transaction.html", {"form": form})

@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect('transaction_list')
    else:
        form = CategoryForm()
    return render(request, 'core/add_category.html', {'form': form})

@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.delete()
    return redirect("my_categories")

@login_required
def analytics(request):
    user = request.user
    # Фильтры из GET-параметров (например, ?period=month)
    period = request.GET.get('period', 'month')
    today = date.today()
    if period == 'day':
        date_from = today
    elif period == 'week':
        date_from = today - timedelta(days=7)
    elif period == 'year':
        date_from = today - timedelta(days=365)
    else:  # месяц по умолчанию
        date_from = today - timedelta(days=30)

    df = get_transactions_df(user, date_from=date_from)
    category_stats = category_report(df)
    if df.empty or 'amount' not in df.columns:
        return render(request, "utils/analytics.html", {
            "warning": "Нет данных для отображения.",
            "income_expense_plot": None,
            "expense_pie_plot": None,
            "stats": {},
            "anomalies": [],
            "advices": [],
            'category_stats': category_stats,
            })
    stats = calculate_stats(df)
    # stats['total_income'], stats['total_expense'], stats['balance']
    anomalies = detect_anomalies(df)
    advices = generate_advice(df)
    img_income_expense = plot_income_expense(df)
    img_expense_pie = plot_expense_pie(df)

    return render(request, 'utils/analytics.html', {
        'img_income_expense': img_income_expense,
        'img_expense_pie': img_expense_pie,
        'stats': stats, 'anomalies': anomalies,
        'advices': advices, 'category_stats': category_stats,
    })

@login_required
def profile_view(request):
    try:
        profile = request.user.telegramprofile
    except TelegramProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = TelegramProfileForm(request.POST, instance=profile)
        if form.is_valid():
            telegram_profile = form.save(commit=False)
            telegram_profile.user = request.user
            telegram_profile.save()
            return redirect('/')
    else:
        form = TelegramProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'form': form})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # создаём пользователя
            login(request, user)  # сразу логиним
            return redirect('transaction_list')  # редиректим на список операций
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})










