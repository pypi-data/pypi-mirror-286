from django.db import models
import uuid
from ..constants.user_constants import USER_GENDER_CHOICES


class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=255)
    phone_number = models.CharField()
    gender = models.TextChoices(USER_GENDER_CHOICES)
    age = models.IntegerField()
    date_of_birth = models.DateField()