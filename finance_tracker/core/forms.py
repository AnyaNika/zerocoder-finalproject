from django import forms
from .models import Transaction


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "date", "type", "category", "description"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }