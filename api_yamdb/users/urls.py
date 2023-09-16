from django.urls import path


from . import views


app_name = 'users'

urlpatterns = [
    path('token/', views.Auth.as_view()),
    path('signup/', views.Signup.as_view())
]
