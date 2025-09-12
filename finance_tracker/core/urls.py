from django.urls import path
from . import views

urlpatterns = [
    path("", views.transaction_list, name="transaction_list"),
    path("add/", views.add_transaction, name="add_transaction"),
    path('register/', views.register, name='register'),  # регистрация
    path('add_category/', views.add_category, name='add_category'),
    path("my_categories/", views.my_categories, name="my_categories"),
    path("delete_category/<int:pk>/", views.delete_category, name="delete_category"),
]
