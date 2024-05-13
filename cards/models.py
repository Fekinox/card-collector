from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    value = models.IntegerField()
    deck = models.ForeignKey(
        'decks.Deck',
        related_name='cards',
        on_delete=models.CASCADE,
        null=False,
    )
