from django import forms
from .models import Transaction, Category


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ["amount", "date", "type", "category"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)  # <-- передадим user в форму
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
