from django.db.models import Model
from django.db.models.query import QuerySet


def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()
