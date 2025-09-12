from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import Transaction, Category
from .forms import TransactionForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by("-date")
    return render(request, "core/transaction_list.html", {"transactions": transactions})

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










