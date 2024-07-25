class Cards:
    def __init__(self):
        self.cards = []

    def add_card(self, card: dict):
        self.cards.append(card)

    def get_cards(self):
        return self.cards