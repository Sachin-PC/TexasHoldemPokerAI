from Models.Player import Player
# from Models.StandardDeck import StandardDeck
import itertools

from Models.StandardDeck import StandardDeck


class Game:
    isItStatic = "xyz"
    hand_max_cards = 5

    def __init__(self, list_of_players):
        self.no_of_games = 0
        self.community_cards = []
        self.list_of_players = list_of_players
        self.small_blind = 10
        self.big_blind = 20
        self.deck = None

    def cardDetails(self):
        print("card details = ", self.cards, "  check static = ", self.isItStatic)

    def play(self):
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        no_rounds_completed = 0
        total_pot = 0
        if self.no_of_games%2 == 0:
            player1 = self.list_of_players.get(0);
            player2 = self.list_of_players.get(1);
        else:
            player1 = self.list_of_players.get(1);
            player2 = self.list_of_players.get(0);
        player1.increase_bet(self.small_blind)
        player2.increase_bet(self.big_blind)
        # total_pot += self.small_blind + self.big_blind;

        # round 1
        self.dealcards(player1,player2)
        bet_raised = self.raisebets(player1, player2)
        if bet_raised[1] == 0:
            total_pot += self.small_blind + self.big_blind + bet_raised[0]
        else:
            if bet_raised[1] == 1:
                return player1
            else:
                return player2

        # round 2
        self.dealCommunityCards(3)
        bet_raised = self.raisebets(player1, player2)
        if bet_raised[1] == 0:
            total_pot += bet_raised[0]
        else:
            if bet_raised[1] == 1:
                return player1
            else:
                return player2

        # round 3
        self.dealCommunityCards(1)
        bet_raised = self.raisebets(player1, player2)
        if bet_raised[1] == 0:
            total_pot += bet_raised[0]
        else:
            if bet_raised[1] == 1:
                return player1
            else:
                return player2

        #round 4
        self.dealCommunityCards(1)
        bet_raised = self.raisebets(player1, player2)
        if bet_raised[1] == 0:
            total_pot += bet_raised[0]
        else:
            if bet_raised[1] == 1:
                return player1
            else:
                return player2

        #showdown
        self.showdown(player1,player2)


    def raisebets(self,player1, player2):

        total_bet_raised = []
        bet_raised = 0
        player1_bet_option = input("Enter Your Bet Option! 1.Bet 2.Fold 3.Check")
        player1_bet = 0
        if player1_bet_option == 1:
            player1_bet = input("Enter Your Bet")
            bet_raised = player1_bet
        elif player1_bet_option == 2:
            total_bet_raised.append(0)
            total_bet_raised.append(2)
            return

        player2_bet_option = input("Enter Your Bet Option! 1.Bet 2.Fold 3.Check 4.Call 5.Raise")
        player1_bet = 0
        if player1_bet_option == 1:
            player1_bet = input("Enter Your Bet")
            bet_raised += player1_bet
        elif player2_bet_option == 2:
            total_bet_raised.append(bet_raised)
            total_bet_raised.append(1)
            return
        elif player2_bet_option == 4:
            bet_raised += bet_raised
        elif player2_bet_option == 5:
            player1_bet = input("Enter Your Raise Amount")
            bet_raised += bet_raised + player1_bet

        total_bet_raised.append(bet_raised)
        total_bet_raised.append(0)

    def dealCommunityCards(self,no_of_cards):
        for i in range(no_of_cards):
            self.community_cards.append(self.deck.deal())

    def dealcards(self,player1,player2):
        player1.cards.append(self.deck.deal())
        player2.cards.append(self.deck.deal())
        player1.cards.append(self.deck.deal())
        player2.cards.append(self.deck.deal())

    def showdown(self,player1,player2):
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())
        self.community_cards.append(self.deck.deal())
        print("Community cards = ",self.community_cards)
        card_combinations = []
        total_cards = 5
        player1_bestrank = 20
        player2_bestrank = 20
        player1_card_combinations = []
        player2_card_combinations = []
        # getPlayerRanking(player1)
        # getPLayerRanking(player2)
        # for no_of_cards in range(2):
        #     for player_card_combination in itertools.combinations(player1.cards, no_of_cards):
        #         for community_card_combination in itertools.combinations(self.community_cards, total_cards-no_of_cards):
        #             card_combinations = player_card_combination + community_card_combination
        #             player1_rank = self.checkPokerHandRanking(card_combinations)
        #             if player1_rank < player1_bestrank:
        #                 player1_bestrank = player1_rank

        for no_of_cards in range(3):
            for player_card_combination in itertools.combinations(player1.cards, no_of_cards):
                player1_card_combinations.append(player_card_combination)
        for no_of_cards in range(3):
            for player_card_combination in itertools.combinations(player2.cards, no_of_cards):
                player2_card_combinations.append(player_card_combination)

        print("player1_card_combinations = ",player1_card_combinations)

        j = 0;
        for i in range(4):
            player1_card_combination = player1_card_combinations[i]
            player2_card_combination = player2_card_combinations[i]
            print("player1_card_combination = ",player1_card_combination)
            print("player2_card_combination = ", player2_card_combination)
            no_of_req_cards = total_cards - len(player1_card_combination)
            print("no of required cards = ",no_of_req_cards)

            for community_card_combination in itertools.combinations(self.community_cards, no_of_req_cards):
                print("community card combinations = ",community_card_combination)
                p1_card_comb = player1_card_combination + community_card_combination
                p2_card_comb = player2_card_combination + community_card_combination
                print(p1_card_comb)
                print(p2_card_comb)
                player1_rank = self.checkPokerHandRanking(p2_card_comb)
                if player1_rank < player1_bestrank:
                    player1_bestrank = player1_rank

                player2_rank = self.checkPokerHandRanking(p2_card_comb)
                if player2_rank < player2_bestrank:
                    player2_bestrank = player2_rank

                j = j+1

        print("j = ",j)
        print("player1 rank = ",player1_bestrank)
        print("player2 rank = ", player2_bestrank)

        # for player_card in player1.cards:
        #     card_combinations.append(player_card)
        #     combinations = itertools.combinations(self.community_cards,4)
        #     for community_card in self.community_cards:

        # player1_rank = self.checkPokerHandRanking(player1.ca)



    def checkPokerHandRanking(self, cards_as_set):

        cards = list(cards_as_set)
        poker_hand = None
        same_suit = True

        pair = 0
        pair_highest_rank = None
        three_of_a_kind = 0
        three_of_a_kind_highest_rank = None
        four_of_a_kind = 0
        four_of_a_kind_highest_rank = None

        same_rank_card_count = 1
        continuous_card_count = 1

        cards.sort(key=lambda x: x.rank_value)
        for card in cards:
            print(card.rank, " of ", card.suit_name, " val = ", card.rank_value)
        prev_rank_value = None
        hand_suit = None
        for card in cards:
            if prev_rank_value is None:
                same_rank_card_count = 1
                hand_suit = card.suit_name
                continuous_card_count = 1
                prev_rank_value = card.rank_value
            else:
                if card.suit_name != hand_suit:
                    same_suit = False
                if card.rank == prev_rank_value:
                    same_rank_card_count += 1
                else:
                    if same_rank_card_count == 2:
                        pair += 1
                        pair_highest_rank = prev_rank_value
                    elif same_rank_card_count == 3:
                        three_of_a_kind = 1
                        three_of_a_kind_highest_rank = prev_rank_value
                    elif same_rank_card_count == 4:
                        four_of_a_kind = 1
                        four_of_a_kind_highest_rank = prev_rank_value

                    prev_rank = card.rank_value
                    same_rank_card_count = 1

                    if card.rank_value == prev_rank_value + 1:
                        continuous_card_count += 1
                    else:
                        continuous_card_count = 1

        if continuous_card_count == self.hand_max_cards:
            if same_suit:
                if prev_rank_value == 14:
                    poker_hand = "Royal Flush"
                    poker_hand_rank = 1
                else:
                    poker_hand = "Straight Flush"
                    poker_hand_rank = 2
            else:
                poker_hand = "Straight"
                poker_hand_rank = 6
        elif four_of_a_kind == 1:
            poker_hand = "Four of A Kind"
            poker_hand_rank = 3
        elif three_of_a_kind == 1:
            if pair == 1:
                poker_hand = "Full house"
                poker_hand_rank = 4
            else:
                poker_hand = "Three of a Kind"
                poker_hand_rank = 7
        elif same_suit:
            poker_hand = "Flush"
            poker_hand_rank = 5
        elif pair == 2:
            poker_hand = "Two Pair"
            poker_hand_rank = 8
        elif pair == 1:
            poker_hand = "Pair"
            poker_hand_rank = 9
        else:
            poker_hand = "High Card"
            poker_hand_rank = 10

        return poker_hand_rank


# deck = StandardDeck()
# deck.shuffle_cards()
# # cards = deck.get_cards()
# game1 = Game("testCards", "2players");
# game1.checkPokerHandRanking(deck.cards)

# player1 = Player("Human")
# player2 = Player("Human")
# player1.cards.append(deck.deal())
# player1.cards.append(deck.deal())
# player2.cards.append(deck.deal())
# player2.cards.append(deck.deal())

# game2 = Game("testCards2", "3players");
# game1.cardDetails();
# game2.cardDetails();

deck = StandardDeck()
deck.shuffle_cards()
print(deck.cards)

player1 = Player("Human")
player2 = Player("Human")
player1.cards.append(deck.deal())
player1.cards.append(deck.deal())
player2.cards.append(deck.deal())
player2.cards.append(deck.deal())

print(player1.cards)
print(player2.cards)

game = Game([player1,player2])

print(game.list_of_players[0].cards)
game.showdown(player1,player2)
