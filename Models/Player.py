class Player(object):

    def __init__(self, player_type):
        self.player_type = player_type
        self.player_name = "xyx"
        self.cards = []
        self.chips = 0
        self.fold = False
        self.bet = 0
        self.win = False

    def add_card(self, card):
        self.cards.append(card)

    def get_cards(self):
        return self.cards

    def get_bet_amount(self):
        return self.bet

    def increase_bet(self, bet_amount):
        self.bet += bet_amount
        self.chips -= bet_amount

    def increase_chips(self, chips_won):
        self.chips += chips_won

    def set_win(self):
        self.win = True
