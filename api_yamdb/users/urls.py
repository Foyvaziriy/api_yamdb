from django.urls import path

from users import views


urlpatterns = [
    path('token/', views.Auth.as_view()),
    path('signup/', views.Signup.as_view()),
]
