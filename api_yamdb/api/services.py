from django.db.models import Model
from django.db.models.query import QuerySet
from django.utils import timezone


def get_all_objects(model: Model) -> QuerySet:
    return model.objects.all()


def get_current_year() -> int:
    return timezone.now().year
