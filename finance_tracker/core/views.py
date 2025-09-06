from django.shortcuts import render, redirect
from .models import Transaction
from .forms import TransactionForm
from django.contrib.auth.decorators import login_required


@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(owner=request.user).order_by("-date")
    return render(request, "core/transaction_list.html", {"transactions": transactions})


@login_required
def add_transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.owner = request.user
            transaction.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(request, "core/add_transaction.html", {"form": form})