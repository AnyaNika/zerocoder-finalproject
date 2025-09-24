from datetime import date, timedelta
from rest_framework import viewsets, permissions, status
from core.models import Transaction, Category, TelegramProfile
from .serializers import TransactionSerializer, CategorySerializer
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.utils.timezone import now


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def get_queryset(self):
        tg_id = self.request.query_params.get("tg_id")
        date_filter = self.request.query_params.get("date")

        qs = Transaction.objects.all()

        if tg_id:
            try:
                profile = TelegramProfile.objects.get(telegram_id=tg_id)
                qs = qs.filter(user=profile.user)
            except TelegramProfile.DoesNotExist:
                return Transaction.objects.none()

        if date_filter == "today":
            today = now().date()
            qs = qs.filter(date=today)

        return qs

    def create(self, request, *args, **kwargs):
        tg_id = request.data.get("tg_id")
        if not tg_id:
            return Response({"error": "tg_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = TelegramProfile.objects.get(telegram_id=tg_id)
        except TelegramProfile.DoesNotExist:
            return Response({"error": "Telegram profile not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data["user"] = profile.user.id  # привязываем транзакцию к User

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_queryset(self):
        tg_id = self.request.query_params.get("tg_id")
        qs = Category.objects.all()
        if tg_id:
            try:
                profile = TelegramProfile.objects.get(telegram_id=tg_id)
                qs = qs.filter(user=profile.user)
            except TelegramProfile.DoesNotExist:
                return Category.objects.none()
        return qs



@api_view(["POST"])
def register_telegram(request):
    tg_id = request.data.get("tg_id")
    tg_username = request.data.get("username")  # это именно telegram @username

    if not tg_id:
        return Response({"error": "tg_id required"}, status=400)

    # 1. Проверяем, есть ли профиль с таким telegram_id
    profile = TelegramProfile.objects.filter(telegram_id=tg_id).first()
    if profile:
        # Обновим username в профиле, если что-то изменилось
        if tg_username and profile.telegram_username != tg_username:
            profile.telegram_username = tg_username
            profile.save()
        return Response({
            "created": False,
            "username": profile.user.username,
            "message": "Пользователь уже зарегистрирован по этому telegram_id"
        })

    # 2. Если профиля нет, ищем пользователя по User.username
    base_username = tg_username or f"user_{tg_id}"
    user = User.objects.filter(username=base_username).first()

    if user:
        profile = TelegramProfile.objects.create(
            user=user,
            telegram_id=tg_id,
            telegram_username=tg_username
        )
        return Response({
            "created": True,
            "username": user.username,
            "message": "Создан профиль Telegram для существующего пользователя"
        })

    # 3. Если такого пользователя нет — создаём нового
    user = User.objects.create(username=base_username)
    profile = TelegramProfile.objects.create(
        user=user,
        telegram_id=tg_id,
        telegram_username=tg_username
    )
    return Response({
        "created": True,
        "username": user.username,
        "message": "Создан новый пользователь и привязан telegram_id"
    })