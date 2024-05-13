from rest_framework import generics
from cards.models import Card, Deck, Ability
from cards.serializers import (
    CardSerializer, DeckSerializer, SubCardSerializer, AbilitySerializer
)
from rest_framework import status
from rest_framework.views import Response


class DeckList(generics.ListCreateAPIView):
    permission_classes = []

    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Pop off the cards from the request data
        cards = request.data.pop('cards')

        # Create the deck
        deck_ser = DeckSerializer(data=request.data)
        if not deck_ser.is_valid():
            return Response(
                deck_ser.errors, status=status.HTTP_400_BAD_REQUEST
            )
        deck = deck_ser.save()

        # Create each card
        for card in cards:
            ability_elem = card.pop('abilities')

            new_card = Card.objects.create(deck=deck, **card)

            for ability in ability_elem:
                new_ability, created = Ability.objects.get_or_create(name=ability['name'], defaults=ability)
                new_card.abilities.add(new_ability)

        return Response(deck_ser.data, status=status.HTTP_201_CREATED)


class CardList(generics.ListCreateAPIView):
    permission_classes = []

    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []

    queryset = Card.objects.all()
    serializer_class = CardSerializer


class DeckCardList(generics.ListAPIView):
    permission_classes = []

    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(deck_id=self.kwargs['pk'])

    def post(self, request, pk):
        serializer = SubCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(deck_id=pk)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeckDetail(generics.RetrieveAPIView):
    permission_classes = []

    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class AbilityList(generics.ListCreateAPIView):
    permission_classes = []

    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer
