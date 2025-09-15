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
    username = request.data.get("username")

    if not tg_id:
        return Response({"error": "tg_id required"}, status=400)

    # fallback для пустого username
    if not username:
        username = f"user_{tg_id}"

    # 1. Проверяем, есть ли профиль с таким telegram_id
    profile = TelegramProfile.objects.filter(telegram_id=tg_id).first()
    if profile:
        return Response({
            "created": False,
            "username": profile.user.username,
            "message": "Пользователь уже был зарегистрирован по этому telegram_id"
        })

    # 2. Если профиля нет, ищем пользователя по username
    user = User.objects.filter(username=username).first()
    if user:
        # Проверяем, есть ли у него уже профиль
        profile = TelegramProfile.objects.filter(user=user).first()
        if profile:
            # Обновляем существующий профиль
            profile.telegram_id = tg_id
            profile.save()
            return Response({
                "created": False,
                "username": user.username,
                "message": "telegram_id обновлён для существующего пользователя"
            })
        else:
            # Создаём новый профиль для пользователя
            profile = TelegramProfile.objects.create(user=user, telegram_id=tg_id)
            return Response({
                "created": True,
                "username": user.username,
                "message": "Создан профиль Telegram для существующего пользователя"
            })

    # 3. Если такого пользователя нет — создаём нового
    user = User.objects.create(username=username)
    profile = TelegramProfile.objects.create(user=user, telegram_id=tg_id)
    return Response({
        "created": True,
        "username": user.username,
        "message": "Создан новый пользователь и привязан telegram_id"
    })