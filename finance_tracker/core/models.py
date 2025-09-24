from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Category(models.Model):
   name = models.CharField(max_length=100)
   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories") # 🔑 привязка к пользователю

   def __str__(self):
       return self.name


class Transaction(models.Model):
   TYPE_CHOICES = (
       ("income", "Доход"),
       ("expense", "Расход"),
   )

   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions")
   amount = models.DecimalField(max_digits=10, decimal_places=2)
   date = models.DateField()
   type = models.CharField(max_length=7, choices=TYPE_CHOICES)
   category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
   description = models.TextField(blank=True, null=True)

   def __str__(self):
       return f"{self.type}: {self.amount} ({self.category})"


class TelegramProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telegram_id = models.BigIntegerField(unique=True)
    telegram_username = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} ↔ {self.telegram_id}"

