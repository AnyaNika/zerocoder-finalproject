from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet, CategoryViewSet, register_telegram

router = DefaultRouter()

router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path("", include(router.urls)),
    path("register_telegram/", register_telegram, name="register_telegram"),
]