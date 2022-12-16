import pickle
import csv

class FileOperations(object):

    def __init__(self):
        self.regret_values_pickle_file_path = "/Users/sachinpc/PycharmProjects/FAI/TexasHoldemPoker/DictionaryFiles" \
                                              "/regret_values_pickle_file.pickle"
        self.regret_values_csv_file_path = "/Users/sachinpc/PycharmProjects/FAI/TexasHoldemPoker/DictionaryFiles" \
                                           "/regret_values_csv_file.csv"

    def save_regret_values_into_pickle_file(self, regret_values_dict):
        pickle_file = open(self.regret_values_pickle_file_path, "wb")
        pickle.dump(regret_values_dict, pickle_file)
        pickle_file.close()

    def get_regret_values_from_pickle_file(self):
        pickle_file = open(self.regret_values_pickle_file_path, "rb")
        regret_values_dict = pickle.load(pickle_file)
        pickle_file.close()
        return regret_values_dict

    def save_regret_values_into_csv_file(self, regret_values_dict):
        csv_file = csv.writer(open(self.regret_values_csv_file_path, "w"))
        for key, val in regret_values_dict.items():
            csv_file.writerow([key, val])
