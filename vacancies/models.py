from django.db import models


class Vacancy(models.Model):
    text = models.CharField(max_length=2000)
