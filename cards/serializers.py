from rest_framework import serializers
from django.contrib.auth.models import User
from cards.models import Card, Deck, Ability


class AbilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Ability
        fields = '__all__'


class CardSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=False)

    class Meta:
        model = Card
        fields = '__all__'


class SubCardSerializer(serializers.ModelSerializer):
    abilities = AbilitySerializer(many=True, read_only=True)

    class Meta:
        model = Card
        fields = [
            'id', 'name', 'description', 'value',
            'health', 'damage', 'cost', 'abilities'
        ]


class DeckSerializer(serializers.ModelSerializer):
    cards = SubCardSerializer(many=True, read_only=True)

    class Meta:
        model = Deck
        fields = ['id', 'name', 'cards']


class UserSerializer(serializers.ModelSerializer):
    decks = DeckSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'decks']
