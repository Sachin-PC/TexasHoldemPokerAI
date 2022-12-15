from Models.FileOperations import FileOperations
from Models.Player import Player
import random
# from Models.StandardDeck import StandardDeck
import itertools

from Models.StandardDeck import StandardDeck


class Game:
    hand_max_cards = 5

    def __init__(self, list_of_players):
        self.no_of_games = 0
        self.community_cards = []
        self.list_of_players = list_of_players
        self.small_blind = 10
        self.big_blind = 20
        self.deck = None
        self.total_pot = 0
        self.identical_card_abstraction = []
        self.unique_card_abstractions = {}
        self.get_unique_cards_abstraction()
        self.card_abstractions_from_file = {}

    # def card_details(self):
    #     print("card details = ", self.cards, "  check static = ", self.isItStatic)

    def perform_regret_iterations(self,no_of_iterations):
        for i in range(no_of_iterations):
            print("Iteration ",i)
            self.deck = None
            self.community_cards = []
            for player in self.list_of_players:
                player.cards = []
                player.win = False
            self.play(0)

        file_operations = FileOperations()
        file_operations.save_regret_values_into_pickle_file(self.unique_card_abstractions)
        file_operations.save_regret_values_into_csv_file(self.unique_card_abstractions)
        regretvals = file_operations.get_regret_values_from_pickle_file()
        # print(regretvals)
        # print("len of regret vals = ", len(regretvals))

    def play_texas_holdem(self,no_of_games):

        for player in self.list_of_players:
            player.cards = []
            player.chips = 1000000
            player.bet = 0
        file_operations = FileOperations()
        self.card_abstractions_from_file = file_operations.get_regret_values_from_pickle_file()
        self.no_of_games = 0
        for i in range(no_of_games):
            self.no_of_games = i
            self.deck = None
            self.community_cards = []
            for player in self.list_of_players:
                player.cards = []
                player.win = False
            self.play(1)
        p_i=1
        print("After ", no_of_games, " Games:")
        for player in self.list_of_players:
            print("Chips with player ",p_i," = ",player.chips)
            p_i +=1

        if self.list_of_players[0].chips > self.list_of_players[1].chips:
            return 1
        else:
            return 0
    def play(self,play_type):

        self.total_pot = 0
        self.deck = StandardDeck()
        self.deck.shuffle_cards()
        no_rounds_completed = 0
        # total_pot = 0
        # if self.no_of_games % 2 == 0:
        #     cur_game_player1 = self.list_of_players[0];
        #     cur_game_player2 = self.list_of_players[1];
        # else:
        #     cur_game_player1 = self.list_of_players.get[1];
        #     cur_game_player2 = self.list_of_players.get[1];
        cur_game_player1 = self.list_of_players[0];
        cur_game_player2 = self.list_of_players[1];
        cur_game_player1.increase_bet(self.small_blind)
        cur_game_player2.increase_bet(self.big_blind)
        self.total_pot += self.small_blind + self.big_blind;

        # round 1
        # print("Round 1")
        self.deal_cards(cur_game_player1, cur_game_player2)
        # print("Cards dealt for players")
        # print("player 1 cards = ", cur_game_player1.get_cards())
        # print("player 2 cards = ", cur_game_player2.get_cards())
        game_finished = self.play_round(cur_game_player1, cur_game_player2,play_type,1)
        if game_finished:
            # print("Game over")
            return

        # round 2
        # print("Round 2")
        self.deal_community_cards(3)
        # print("Community cards are:\n",self.community_cards)
        game_finished = self.play_round(cur_game_player1, cur_game_player2,play_type,2)
        if game_finished:
            # print("Game over")
            return

        # round 3
        # print("Round 3")
        self.deal_community_cards(1)
        # print("Community cards are:\n", self.community_cards)
        game_finished = self.play_round(cur_game_player1, cur_game_player2,play_type,3)
        if game_finished:
            # print("Game over")
            return

        # round 4
        # print("Round 4")
        self.deal_community_cards(1)
        game_finished = self.play_round(cur_game_player1, cur_game_player2,play_type,4)
        if game_finished:
            # print("Game over")
            return

        # showdown
        # print("Showdown")
        self.showdown(cur_game_player1, cur_game_player2)

    def play_round(self, cur_game_player1, cur_game_player2, play_type, round_no):
        bet_raised = self.raise_bets(cur_game_player1, cur_game_player2,play_type,round_no)
        # print("Bet Raised in 1st round = ", bet_raised)
        # print("Player 1 total bet = ", player1.get_bet_amount())
        # print("Player 2 total bet = ", player2.get_bet_amount())
        if bet_raised[1] == 0:
            self.total_pot += bet_raised[0]
        else:
            if bet_raised[1] == 1:
                cur_game_player1.increase_chips(self.total_pot + bet_raised[0])
                return True
            else:
                cur_game_player2.increase_chips(self.total_pot + bet_raised[0])
                return True
        # print("Total pot after this round = ", self.total_pot)
        return False

    def raise_bets(self, player1, player2,play_type,round_no):

        if play_type == 0:
            total_bet_raised = [40, 0]
            return total_bet_raised
        if play_type == 1:
            raise_values = [10,20,30,40,50]
            total_bet_raised = []
            bet_raised = 0
            # player1_bet_option = int(input("Enter Your Bet Option!\n1.Bet 2.Fold 3.Check\n"))
            # if player1_bet_option == 1:
            #     player1_bet = int(input("Enter Your Bet\n"))
            #     bet_raised = player1_bet
            # elif player1_bet_option == 2:
            #     total_bet_raised.append(0)
            #     total_bet_raised.append(2)
            #     return total_bet_raised
            if round_no > 1:
                player_card_combinations_with_community_cards = self.get_card_combinations(player1)
                # print("player_card_combinations")
                best_reward = self.get_best_regret_reward_comb(player_card_combinations_with_community_cards)
                if best_reward < 0:
                    total_bet_raised.append(bet_raised)
                    total_bet_raised.append(1)
                    return total_bet_raised
                else:
                    # player1_bet = 20
                    if 0 < best_reward <= 20000:
                        player1_bet = raise_values[1]
                    elif 20000 < best_reward <= 40000:
                        player1_bet = raise_values[2]
                    elif 40000 < best_reward <= 80000:
                        player1_bet = raise_values[3]
                    else:
                        player1_bet = raise_values[4]
                    bet_raised = player1_bet
                    player1.increase_bet(player1_bet)
            else:
                player1_bet = 20
                bet_raised = player1_bet
                player1.increase_bet(player1_bet)

            player2_bet_option = random.randint(1, 3)
            # 1 = Call, 2= Raise, 3=   Fold
            # player2_bet_option = int(input("Enter Your Bet Option! 1.Bet 2.Fold 3.Check 4.Call 5.Raise\n"))
            if player2_bet_option == 1:
                player2_bet = player1_bet
                bet_raised += player2_bet
                player2.increase_bet(player2_bet)
            elif player2_bet_option == 2:
                # player2_bet = 10
                player2_raise_option = random.randint(0, 4)
                player2_bet = raise_values[player2_raise_option]
                player2.increase_bet(bet_raised + player2_bet)
                bet_raised += bet_raised + player2_bet
            elif player2_bet_option == 3:
                total_bet_raised.append(bet_raised)
                total_bet_raised.append(1)
                return total_bet_raised
            # player2.increase_bet(player2_bet)
            total_bet_raised.append(bet_raised)
            total_bet_raised.append(0)
            return total_bet_raised

        # total_bet_raised = []
        # bet_raised = 0
        # player1_bet_option = int(input("Enter Your Bet Option!\n1.Bet 2.Fold 3.Check\n"))
        # if player1_bet_option == 1:
        #     player1_bet = int(input("Enter Your Bet\n"))
        #     bet_raised = player1_bet
        # elif player1_bet_option == 2:
        #     total_bet_raised.append(0)
        #     total_bet_raised.append(2)
        #     return total_bet_raised
        # player1.increase_bet(player1_bet)
        #
        # player2_bet_option = int(input("Enter Your Bet Option! 1.Bet 2.Fold 3.Check 4.Call 5.Raise\n"))
        # if player2_bet_option == 1:
        #     player2_bet = int(input("Enter Your Bet\n"))
        #     bet_raised += player2_bet
        # elif player2_bet_option == 2:
        #     total_bet_raised.append(bet_raised)
        #     total_bet_raised.append(1)
        #     return total_bet_raised
        # elif player2_bet_option == 4:
        #     player2_bet = player1_bet
        #     bet_raised += bet_raised
        # elif player2_bet_option == 5:
        #     player2_bet = int(input("Enter Your Raise Amount\n"))
        #     bet_raised += bet_raised + player2_bet
        # player2.increase_bet(player2_bet)
        # total_bet_raised.append(bet_raised)
        # total_bet_raised.append(0)
        # return total_bet_raised

    def deal_community_cards(self, no_of_cards):
        for i in range(no_of_cards):
            self.community_cards.append(self.deck.deal())

    def deal_cards(self, player1, player2):
        player1.add_card(self.deck.deal())
        player2.add_card(self.deck.deal())
        player1.add_card(self.deck.deal())
        player2.add_card(self.deck.deal())

    def showdown(self, player1, player2):
        # print("Community cards = ", self.community_cards)
        card_combinations = []
        total_cards = 5
        player1_best_rank = 0
        player2_best_rank = 0
        player1_card_combinations = []
        player2_card_combinations = []
        payer1_card_combinations_with_community_cards = []
        player1_rank_list = []
        player2_rank_list = []
        j_val = []

        for no_of_cards in range(3):
            for player_card_combination in itertools.combinations(player1.cards, no_of_cards):
                player1_card_combinations.append(player_card_combination)
        for no_of_cards in range(3):
            for player_card_combination in itertools.combinations(player2.cards, no_of_cards):
                player2_card_combinations.append(player_card_combination)

        # print("player1_card_combinations = ", player1_card_combinations)
        # print("player2_card_combinations = ", player1_card_combinations)

        j = 0;
        for i in range(4):
            player1_card_combination = player1_card_combinations[i]
            player2_card_combination = player2_card_combinations[i]
            # print("player1_card_combination = ", player1_card_combination)
            # print("player2_card_combination = ", player2_card_combination)
            no_of_req_cards = total_cards - len(player1_card_combination)
            # print("no of required cards = ", no_of_req_cards)

            for community_card_combination in itertools.combinations(self.community_cards, no_of_req_cards):
                # print("community card combinations = ", community_card_combination)
                p1_card_comb = player1_card_combination + community_card_combination
                p2_card_comb = player2_card_combination + community_card_combination
                # print(p1_card_comb)
                # print(p2_card_comb)
                payer1_card_combinations_with_community_cards.append(p1_card_comb)
                player1_rank = self.checkPokerHandRanking(p1_card_comb)
                player1_rank_list.append(player1_rank)
                if player1_rank > player1_best_rank:
                    player1_best_rank = player1_rank

                player2_rank = self.checkPokerHandRanking(p2_card_comb)
                player2_rank_list.append(player2_rank)
                if player2_rank > player2_best_rank:
                    player2_best_rank = player2_rank
                j = j + 1
        # print("j = ", j)
        # print("List of player 1 ranks  = ",player1_rank_list)
        # print("List of player 2 ranks  = ", player2_rank_list)
        # print("player1 rank = ", player1_best_rank)
        # print("player2 rank = ", player2_best_rank)
        # print("Player 1 card combinations = ",payer1_card_combinations_with_community_cards)

        if player1_best_rank == player2_best_rank:
            # print("Its a draw")
            player1.increase_chips(self.total_pot / 2)
            player1.set_win()
            player2.increase_chips(self.total_pot / 2)
            player2.set_win()
        elif player1_rank > player2_rank:
            # print("Player 1 is the Winner")
            player1.increase_chips(self.total_pot)
            player1.set_win()
        else:
            # print("Player 2 is the Winner")
            player2.increase_chips(self.total_pot)
            player2.set_win()
        regret_value = player1_best_rank - player2_best_rank
        card_val_list = [0, 0, 0, 0, 0]
        q_index = 0
        for p1_card_combination in payer1_card_combinations_with_community_cards:
            p_index = 0
            for card in p1_card_combination:
                # print("card = ",card)
                card_val_list[p_index] = card.rank_value
                p_index = p_index + 1
            card_val_list.sort()
            card_val_tuple = tuple(card_val_list)
            # print("card_val_tuple = ",card_val_tuple)
            # print("unique abstraction cards = ",self.unique_card_abstractions)
            self.unique_card_abstractions[card_val_tuple] = self.unique_card_abstractions[card_val_tuple] + regret_value
            # print("self.unique_card_abstractions[",card_val_tuple,"] = ",self.unique_card_abstractions[card_val_tuple])
            q_index += 1
        # print("q_index = ",q_index)

    def get_card_combinations(self, player):
        player_card_combinations = []
        player_card_combinations_with_community_cards = []
        for no_of_cards in range(3):
            for player_card_combination in itertools.combinations(player.cards, no_of_cards):
                player_card_combinations.append(player_card_combination)

        for i in range(4):
            player_card_combination = player_card_combinations[i]
            no_of_req_cards = 5 - len(player_card_combination)
            # print("no of required cards = ", no_of_req_cards)

            for community_card_combination in itertools.combinations(self.community_cards, no_of_req_cards):
                p_card_comb = player_card_combination + community_card_combination
                player_card_combinations_with_community_cards.append(p_card_comb)

        return player_card_combinations_with_community_cards

    def get_best_regret_reward_comb(self,player_card_combinations_with_community_cards):
        card_val_list = [0, 0, 0, 0, 0]
        best_reward_value = -1
        for p_card_combination in player_card_combinations_with_community_cards:
            p_index = 0
            for card in p_card_combination:
                card_val_list[p_index] = card.rank_value
                p_index = p_index + 1
            card_val_list.sort()
            card_val_tuple = tuple(card_val_list)
            cards_reward = self.unique_card_abstractions[card_val_tuple]
            if cards_reward > best_reward_value:
                best_reward_value = cards_reward
        return cards_reward


    def checkPokerHandRanking(self, cards_as_set):

        rank_factor = 100
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
        # for card in cards:
        # print(card.rank, " of ", card.suit_name, " val = ", card.rank_value)
        # print("yes", card)
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
                if card.rank_value == prev_rank_value:
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

                    prev_rank_value = card.rank_value
                    same_rank_card_count = 1

                    if card.rank_value == prev_rank_value + 1:
                        continuous_card_count += 1
                    else:
                        continuous_card_count = 1

        # print("continious card count = ", continuous_card_count)
        # print("pairs = ", pair)
        # print("three_of_a_kind", three_of_a_kind)
        # print("four of a kind = ", four_of_a_kind)

        if continuous_card_count == self.hand_max_cards:
            if same_suit:
                if prev_rank_value == 14:
                    poker_hand = "Royal Flush"
                    poker_hand_rank = rank_factor * 10
                else:
                    poker_hand = "Straight Flush"
                    poker_hand_rank = rank_factor * 9 + prev_rank_value
            else:
                poker_hand = "Straight"
                poker_hand_rank = rank_factor * 5 + prev_rank_value
        elif four_of_a_kind == 1:
            poker_hand = "Four of A Kind"
            poker_hand_rank = rank_factor * 8 + four_of_a_kind_highest_rank
        elif three_of_a_kind == 1:
            if pair == 1:
                poker_hand = "Full house"
                poker_hand_rank = rank_factor * 7 + three_of_a_kind_highest_rank * 5 + pair_highest_rank
            else:
                poker_hand = "Three of a Kind"
                poker_hand_rank = rank_factor * 4 + three_of_a_kind_highest_rank
        elif same_suit:
            poker_hand = "Flush"
            poker_hand_rank = rank_factor * 6 + prev_rank_value
        elif pair == 2:
            poker_hand = "Two Pair"
            poker_hand_rank = rank_factor * 3 + pair_highest_rank
        elif pair == 1:
            poker_hand = "Pair"
            poker_hand_rank = rank_factor * 2 + pair_highest_rank
        else:
            poker_hand = "High Card"
            poker_hand_rank = rank_factor
        # print("Its a ", poker_hand, " poker hand rank = ", poker_hand_rank)

        return poker_hand_rank

    def get_unique_cards_abstraction(self):

        cards_count = []
        for p in range(15):
            cards_count.append(0)
            # cards_count[p] = 0
        for i in range(2, 15):
            cards_count[i] += 1
            for j in range(i, 15):
                cards_count[j] += 1
                for k in range(j, 15):
                    cards_count[k] += 1
                    for q in range(k, 15):
                        cards_count[q] += 1
                        for l in range(q, 15):
                            flag = 0
                            cards_count[l] += 1
                            for p in range(14):
                                if cards_count[p] == 5:
                                    flag = 1
                                    break;
                            if flag == 0:
                                card_abstraction = (i, j, k, q, l)
                                self.identical_card_abstraction.append(card_abstraction)
                                self.unique_card_abstractions[card_abstraction] = 0
                                # print(card_abstraction)
                            # else:
                                # print(cards_count)
                            cards_count[l] -= 1
                        cards_count[q] -= 1
                    cards_count[k] -= 1
                cards_count[j] -= 1
            cards_count[i] -= 1
        # print("\n\n\n\nuNQUE CARD ABSTRACTIONS = ",self.unique_card_abstractions)
        # print(len(self.identical_card_abstraction))


c_player1 = Player("Agent")
c_player2 = Player("Human")

game = Game([c_player1, c_player2])
# game.perform_regret_iterations(1000000)
no_of_games = random.randint(500, 10000)
is_p1_win = game.play_texas_holdem(no_of_games)
no_of_wins = 0
for j in range(100):
    no_of_games = random.randint(100, 500)
    is_p1_cash_higher = game.play_texas_holdem(no_of_games)
    print("is_p1_cash_higher = ",is_p1_cash_higher)
    if is_p1_cash_higher:
        no_of_wins += 1

print("No of times p1 cash is higher = ",no_of_wins)
