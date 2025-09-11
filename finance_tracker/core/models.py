from django.db import models
from users.models import User  # 👈 теперь используем кастомного


class Category(models.Model):
    """Категории расходов/доходов"""
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    """Финансовая операция"""
    TRANSACTION_TYPES = (
        ("income", "Доход"),
        ("expense", "Расход"),
    )

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} {self.amount} ({self.category})"

