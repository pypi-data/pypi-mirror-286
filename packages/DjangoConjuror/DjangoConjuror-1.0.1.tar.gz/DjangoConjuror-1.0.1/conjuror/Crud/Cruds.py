from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Model

def StoreData(model: Model, **kwargs):
    """Creates a new record for a given model with error handling."""
    try:
        with transaction.atomic():
            return model.objects.create(**kwargs), None
    except (IntegrityError, ValidationError) as e:
        return None, str(e)

def FetchData(model: Model, **filters):
    """Fetches records from a model based on filters with error handling."""
    try:
        return model.objects.filter(**filters), None
    except Exception as e:
        return None, str(e)

def UpdateData(model: Model, filters, **update_fields):
    """Updates records of a model based on provided filters and update fields with error handling."""
    try:
        with transaction.atomic():
            updated_count = model.objects.filter(**filters).update(**update_fields)
            return updated_count, None
    except (IntegrityError, ValidationError) as e:
        return 0, str(e)

def DeleteData(model: Model, **filters):
    """Deletes records from a model based on filters with error handling."""
    try:
        with transaction.atomic():
            deleted_count, _ = model.objects.filter(**filters).delete()
            return deleted_count, None
    except Exception as e:
        return 0, str(e)
