class Card(object):
    def __init__(self, rank, suit_name, rank_value):
        self.rank = rank
        self.suit_name = suit_name
        self.rank_value = rank_value

    def __repr__(self):
        return str(self.rank)+" of "+str(self.suit_name)+" val = "+str(self.rank_value)
