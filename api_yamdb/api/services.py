from django.db.models import Model
from django.db.models.query import QuerySet

from api_yamdb.reviews import models



def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()
