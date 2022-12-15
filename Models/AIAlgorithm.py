import pickle
import csv

from Models.FileOperations import FileOperations


class AIAlgorithm(object):
    def __init__(self):
        self.identical_card_abstraction = []
        self.unique_card_abstractions = {}

    def get_unique_cards_abstraction(self):

        cards_count = []
        for p in range(15):
            cards_count.append(0)
            # cards_count[p] = 0
        for i in range(2,15):
            cards_count[i] += 1
            for j in range (i,15):
                cards_count[j] += 1
                for k in range(j, 15):
                    cards_count[k] += 1
                    for q in range(k, 15):
                        cards_count[q] += 1
                        for l in range(q,15):
                            flag = 0
                            cards_count[l] += 1
                            for p in range(14):
                                if cards_count[p] == 5:
                                    flag = 1
                                    break;
                            if flag == 0:
                                card_abstraction = (i,j,k,q,l)
                                self.identical_card_abstraction.append(card_abstraction)
                                self.unique_card_abstractions[card_abstraction] = 0
                                print(card_abstraction)
                            else:
                                print(cards_count)
                            cards_count[l] -= 1
                        cards_count[q] -= 1
                    cards_count[k] -= 1
                cards_count[j] -= 1
            cards_count[i] -= 1

        # print("self.unique_card_abstractions: ",self.unique_card_abstractions)
        for x in self.unique_card_abstractions:
            print(x)
            # print(self.unique_card_abstractions[x])
            # print("key = ",x[0]," Value = ",x[1])
        print(len(self.identical_card_abstraction))

algo = AIAlgorithm()
algo.get_unique_cards_abstraction()

dict = {(1,2):1,(2,3):5,(1,2,3,4):7}
y = (1,2)
dict[y] = dict[y] + 10
print(dict)

fop = FileOperations()
fop.save_regret_values_into_pickle_file(algo.unique_card_abstractions)
fop.save_regret_values_into_csv_file(algo.unique_card_abstractions)
regretvals = fop.get_regret_values_from_pickle_file()
print(regretvals)
print("len of regret vals = ",len(regretvals))


