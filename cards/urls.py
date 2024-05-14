from django.urls import path
from cards.views import (
    CardList, CardDetail,
    DeckList, DeckDetail, DeckCardList,
    AbilityList, AbilityDetail,
    UserList, UserDetail,
)

urlpatterns = [
    path('cards/', CardList.as_view(), name="card_list"),
    path('cards/<int:pk>', CardDetail.as_view(), name="card_detail"),
    path('decks/', DeckList.as_view(), name="deck_list"),
    path('decks/<int:pk>', DeckDetail.as_view(), name="deck_detail"),
    path('decks/<int:pk>/cards', DeckCardList.as_view(), name="deck_card_list"),
    path('abilities/', AbilityList.as_view(), name="ability_list"),
    path('abilities/<int:pk>', AbilityDetail.as_view(), name="ability_detail"),
    path('users/', UserList.as_view(), name="user_list"),
    path('users/<str:username>', UserDetail.as_view(), name="user_detail"),
]
