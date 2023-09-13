from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api import views


router = DefaultRouter()
router.register('titles', views.TitleViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
