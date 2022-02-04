from models.card import Card
import random


class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self._build()
        self._shuffle()

    def _build(self):
        for suit in range(4):
            for rank in range(1, 14):
                self.cards.append(Card(suit, rank))

    def _shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return None
        return self.cards.pop()

    def __str__(self) -> str:
        return ", ".join([str(c) for c in self.cards])
