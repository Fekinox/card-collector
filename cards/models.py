from django.db import models


class Deck(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField('auth.User')


class Card(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    value = models.IntegerField()
    deck = models.ForeignKey(
        'cards.Deck',
        related_name='cards',
        on_delete=models.CASCADE,
        null=False,
    )
    health = models.IntegerField()
    damage = models.IntegerField()
    cost = models.IntegerField()
    abilities = models.ManyToManyField('cards.Ability')


class Ability(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )
    description = models.CharField(
        max_length=200,
    )
