from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters, status
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Title
from api.services import get_all_objects
from api.serializers import TitleGETSerilizer, TitlePOSTSerilizer
from api.permissions import IsAdminOrReadOnly

from api_yamdb.api.serializers import CustomUserSerializer


class RegisterUser(APIView):
    def post(self, request: dict) -> Response:
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = super().post(request, *args, **kwargs)
        if response.status_code == status.HTTP_200_OK:
            user = self.user
            refresh = RefreshToken.for_user(user)
            response.data['refresh'] = str(refresh)
            response.data['user_id'] = user.id
            response.data['email'] = user.email
        return response


class TitleViewSet(ModelViewSet):
    queryset = get_all_objects(Title)
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('category__slug', 'genre__slug', 'name', 'year')

    def get_serializer_class(self) -> ModelSerializer:
        if self.request.method == 'GET':
            return TitleGETSerilizer
        return TitlePOSTSerilizer
