from rest_framework import generics
from cards.models import Card
from cards.serializers import CardSerializer


class CardList(generics.ListCreateAPIView):
    permission_classes = []

    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = []

    queryset = Card.objects.all()
    serializer_class = CardSerializer
