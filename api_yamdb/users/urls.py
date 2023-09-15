from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users import views


urlpatterns = [
    path('token/', views.Auth.as_view()),
    path('signup/', views.Signup.as_view())
]
