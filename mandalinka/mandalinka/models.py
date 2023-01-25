# Currently not used, but could be nice to implement to know when things were modified 

from django.db import models

class TimeTrackingMixin():
    date_created = models.DateTimeField(auto_now_add=True, verbose_name="Čas vzniku")
    date_modified = models.DateTimeField(auto_now=True, verbose_name="Naposledy upravené")

class TimeTrackingModel(models.Model, TimeTrackingMixin):
    pass