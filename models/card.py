class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.val = value

    @property
    def value(self) -> int:
        return min(self.val, 10)

    def __str__(self) -> str:
        match self.suit:
            case 0:
                s = '♠'
            case 1:
                s = '♥'
            case 2:
                s = '♦'
            case 3:
                s = '♣'
            case _:
                s = '?'

        match self.val:
            case 1:
                v = 'A'
            case 2:
                v = '2'
            case 3:
                v = '3'
            case 4:
                v = '4'
            case 5:
                v = '5'
            case 6:
                v = '6'
            case 7:
                v = '7'
            case 8:
                v = '8'
            case 9:
                v = '9'
            case 10:
                v = '10'
            case 11:
                v = 'J'
            case 12:
                v = 'Q'
            case 13:
                v = 'K'
            case _:
                v = '?'

        return v + " " + s
