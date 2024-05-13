from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=100)
