from rest_framework import serializers
from cards.models import Card, Deck


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'


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
