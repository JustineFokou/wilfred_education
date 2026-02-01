# education/urls.py
from django.urls import path
from . import views

app_name = "admin"

urlpatterns = [
    path("", views.AdminDashboardView.as_view(), name="dashboard"),
    path("users/create/", views.UserCreateView.as_view(), name="user_create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user_update"),
]