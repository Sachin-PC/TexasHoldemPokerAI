from Models.Card import Card
# from Models.Game import Game
from Models.Player import Player
import random


class StandardDeck:

    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Spades", "Diamonds", "Clubs"]
        values = {"Two": 2, "Three": 3, "Four": 4, "Five": 5, "Six": 6, "Seven": 7, "Eight": 8, "Nine": 9, "Ten": 10,
                  "Jack": 11, "Queen": 12, "King": 13, "Ace": 14}
        for suit in suits:
            for value in values:
                self.cards.append(Card(value, suit, values[value]))

    def get_cards(self):
        for card in self.cards:
            print(card.rank, " of ", card.suit_name, " val = ", card.rank_value)

    def shuffle_cards(self):
        random.shuffle(self.cards)

    def deal(self):
        card = self.cards.pop()
        return card


# deck = StandardDeck()
# deck.shuffle_cards()
# print(deck.cards)
#
# player1 = Player("Human")
# player2 = Player("Human")
# player1.cards.append(deck.deal())
# player1.cards.append(deck.deal())
# player2.cards.append(deck.deal())
# player2.cards.append(deck.deal())
#
# print(player1.cards)
# print(player2.cards)
#
# # game = Game([player1,player2])
# #
# # print(game.list_of_players[0].cards)
# # game.showdown(player1,player2)
#
# # player1 = Player("Human");
# # deck.deal(player1)
# # print("YESS")
# # print(print(player1.cards[0].rank, " of ", player1.cards[0].suit_name, " val = ", player1.cards[0].rank_value))