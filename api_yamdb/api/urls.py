from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from api import views


router = DefaultRouter()

router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet, basename='reviews')
router.register('titles', views.TitleViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]
