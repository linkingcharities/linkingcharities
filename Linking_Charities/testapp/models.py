from django.db import models

class Charity(models.Model):
    name = models.CharField(max_length=200)
    registered_id = models.IntegerField(default=0)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
