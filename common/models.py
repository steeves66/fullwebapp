from django.db import models

class KeyValueStore(models.Model):
    key = models.CharField(max_length=255, unique=True)
    value = models.JSONField()

    def __str__(self):
        return self.key