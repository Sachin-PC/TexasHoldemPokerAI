class Player(object):

    def __init__(self, player_type):
        self.player_type = player_type
        self.player_name = "xyx"
        self.cards = []
        self.chips = 0
        self.fold = False
        self.bet = 0
        self.win = False

    def get_card(self, card):
        self.cards.append(card)

    def increase_bet(self, bet_amount):
        self.bet += bet_amount
        self.chips -= bet_amount
