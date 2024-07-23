from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminLoginView

router = DefaultRouter()

urlpatterns = [
    path("", include(router.urls)),
    path("login", AdminLoginView.as_view(), name="admin-login"),
]
