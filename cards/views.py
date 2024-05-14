from rest_framework import generics
from cards.models import Card, Deck, Ability
from django.contrib.auth.models import User
from cards.serializers import (
    CardSerializer, DeckSerializer, SubCardSerializer, AbilitySerializer,
    UserSerializer,
)
from rest_framework import status
from rest_framework.views import Response
from django.db import transaction

from auth.permissions import IsAdminOrOwningUserOrAnonReadOnly


class DeckList(generics.ListCreateAPIView):
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
                # If an ability already exists with the given name, retrieve it.
                # Otherwise, create a new ability with the same name and the
                # given description.
                new_ability, created = Ability.objects.get_or_create(
                    name=ability['name'],
                    defaults=ability
                )
                new_card.abilities.add(new_ability)

        return Response(deck_ser.data, status=status.HTTP_201_CREATED)


class CardList(generics.ListCreateAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class CardDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer


class DeckCardList(generics.ListAPIView):
    serializer_class = CardSerializer

    def get_queryset(self):
        return Card.objects.filter(deck_id=self.kwargs['pk'])

    def post(self, request, pk):
        serializer = SubCardSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save(deck_id=pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DeckDetail(generics.RetrieveAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer


class AbilityList(generics.ListCreateAPIView):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class AbilityDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ability.objects.all()
    serializer_class = AbilitySerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class UserFavoritesList(generics.ListAPIView):
    def get_queryset(self):
        return User.objects.get(username=self.kwargs['username']).deck_set.all()

    serializer_class = DeckSerializer


class UserFavoritesDetail(generics.RetrieveAPIView):
    permission_classes = [IsAdminOrOwningUserOrAnonReadOnly]

    def get_queryset(self):
        return User.objects.get(username=self.kwargs['username']).deck_set.all()

    serializer_class = DeckSerializer
    lookup_field = 'pk'

    def put(self, request, username, pk):
        user = User.objects.get(username=username)
        self.check_object_permissions(request, user)
        deck = Deck.objects.get(pk=pk)
        if user.deck_set.filter(pk=pk).exists():
            return Response({
                "message": f"Deck {pk} is already in {username}'s favorites"
            })

        user.deck_set.add(deck)
        return Response({
            "message": f"Added deck {pk} to {username}'s favorites"
        })

    def delete(self, request, username, pk):
        user = User.objects.get(username=username)
        self.check_object_permissions(request, user)
        deck = Deck.objects.get(pk=pk)
        if not user.deck_set.filter(pk=pk).exists():
            return Response({
                "message": f"Deck {pk} is not in {username}'s favorites"
            })

        user.deck_set.remove(deck)
        return Response({
            "message": f"Removed deck {pk} from {username}'s favorites"
        })
