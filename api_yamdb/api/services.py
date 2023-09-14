from django.db.models import Model
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404


def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()


def query_with_filter(model: Model,
                      filter_dict: dict,
                      single=False) -> QuerySet:
    if single:
        return get_object_or_404(
            model,
            **filter_dict
        )
    else:
        return model.objects.filter(
            **filter_dict
        )
