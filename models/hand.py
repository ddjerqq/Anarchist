from models.card import Card


class Hand:
    def __init__(self, cards: list[Card] = None):
        self.cards: list[Card] = cards if cards else []

    @property
    def sum(self):
        return sum([card.value for card in self.cards])

    @property
    def value(self):
        if self.has_ace and self.sum <= 11:
            return self.sum + 10
        return self.sum

    @property
    def has_ace(self):
        return 1 in [card.val for card in self.cards]

    def add_card(self, card: Card):
        self.cards.append(card)
        return card

    @property
    def str_cards(self):
        return " ".join([str(card) for card in self.cards])
