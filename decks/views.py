from rest_framework import generics
from decks.models import Deck
from cards.models import Card
from decks.serializers import DeckSerializer, SubCardSerializer
from cards.serializers import CardSerializer
from rest_framework import status
from rest_framework.views import Response


class DeckList(generics.ListCreateAPIView):
    permission_classes = []

    queryset = Deck.objects.all()
    serializer_class = DeckSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


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
