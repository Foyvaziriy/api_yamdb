from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import MethodNotAllowed


class NoPutViewSetMixin(GenericViewSet):
    def update(self, request, *args, **kwargs):
        if request.method == 'PUT':
            raise MethodNotAllowed(request.method)

        return super().update(request, *args, **kwargs)
