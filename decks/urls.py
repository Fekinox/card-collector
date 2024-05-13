from django.urls import path
from decks.views import DeckList, DeckDetail, DeckCardList

urlpatterns = [
    path('', DeckList.as_view(), name="deck_list"),
    path('<int:pk>', DeckDetail.as_view(), name="deck_detail"),
    path('<int:pk>/cards', DeckCardList.as_view(), name="deck_card_list"),
]
