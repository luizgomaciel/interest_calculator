import uuid

from django.db import models

class InitialProjectModel(models.Model):
    id = models.UUIDField(primary_key=True, default=str(uuid.uuid4))
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'initial_projects'

    def __str__(self):
        return self.name
