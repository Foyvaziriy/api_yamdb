from django.db.models import Model, Avg
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404

from reviews.models import Title


def get_or_create(model: Model, **kwargs) -> (Model, bool):
    return model.objects.get_or_create(**kwargs)


def create_object(model: Model, **parameters) -> Model:
    return model.objects.create(**parameters)


def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()


def query_with_filter(
    model: Model, filter_dict: dict, single=False
) -> QuerySet:
    if single:
        return get_object_or_404(model, **filter_dict)
    else:
        return model.objects.filter(**filter_dict)


def query_title_with_rating() -> QuerySet:
    return Title.objects.annotate(rating=Avg('reviews__score'))
