from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ActivatableModel(models.Model):
    is_active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True

    def change_status(self):
        if self.is_active:
            self.is_active = False
        else:
            self.is_active = True
