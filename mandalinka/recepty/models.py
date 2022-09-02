from django.db import models

# Create your models here.

class Recipe_mod(models.Model):
    title = models.CharField(max_length=20)
    prep_time = models.IntegerField()

    def __str__(self):
        return f"{self.id}: {self.title} taking {self.prep_time} mins to prepare"