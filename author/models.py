from django.db import models


class Author(models.Model):
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField()
    bio = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['first_name']),
        ]

    def __str__(self):
        return self.first_name
    
    def fetch_short_bio(self):
        return self.bio[:6]