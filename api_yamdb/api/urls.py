from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    views.CommentViewSet, basename='comments')
router.register(r'titles/(?P<title_id>\d+)/reviews',
                views.ReviewViewSet, basename='reviews')
router.register('titles', views.TitleViewSet)
router.register('categories', views.CategoryViewSet)
router.register('genres', views.GenreViewSet)
router.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('users.urls'))
]
