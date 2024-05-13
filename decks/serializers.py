from rest_framework import serializers
from decks.models import Deck
from cards.models import Card
import logging
logger = logging.getLogger(__name__)


class SubCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'name', 'description', 'value']


class DeckSerializer(serializers.ModelSerializer):
    cards = SubCardSerializer(many=True)

    class Meta:
        model = Deck
        fields = ['id', 'name', 'cards']

    def create(self, validated_data):
        cards_data = validated_data.pop('cards')
        deck = Deck.objects.create(**validated_data)
        deck.cards.bulk_create(
            Card(deck=deck, **card)
            for card in cards_data
        )
        return deck
