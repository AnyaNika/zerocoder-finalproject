from datetime import date, timedelta
from rest_framework import viewsets, permissions
from core.models import Transaction, Category, TelegramProfile
from .serializers import TransactionSerializer, CategorySerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Transaction.objects.all()
        tg_id = self.request.query_params.get("tg_id")
        date_param = self.request.query_params.get("date")
        category_param = self.request.query_params.get("category")

        if tg_id:
            try:
                profile = TelegramProfile.objects.get(telegram_id=tg_id)
                qs = qs.filter(user=profile.user)
            except TelegramProfile.DoesNotExist:
                return Transaction.objects.none()

        if date_param == "today":
            qs = qs.filter(date=date.today())
        elif date_param == "week":
            week_ago = date.today() - timedelta(days=7)
            qs = qs.filter(date__gte=week_ago)

        if category_param:
            qs = qs.filter(category__name__iexact=category_param)

        return qs


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)



@api_view(["POST"])
def register_telegram(request):
    tg_id = request.data.get("tg_id")
    username = request.data.get("username") or f"user_{tg_id}"

    if not tg_id:
        return Response({"error": "tg_id required"}, status=400)

    profile, created = TelegramProfile.objects.get_or_create(
        telegram_id=tg_id,
        defaults={
            "user": User.objects.create(username=username)
        }
    )

    return Response({
        "created": created,
        "username": profile.user.username
    })