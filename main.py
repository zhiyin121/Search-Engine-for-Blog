from get_data import GroupData, get_filename, clean_data, get_data
from analysis_query import clean_query, AugmentedQuery

import os
import pickle


class SearchEngine:
    def __init__(self):
        return
        
    def load_corpus(self, filepath, local_filepath, pickle_path):
        data_lists = []
        filename_list = get_filename(filepath)
        index = 0
        for filename in filename_list:
            #clean_data(filepath, filename)
            data_list, index = get_data(local_filepath, filename, index)
            data_lists += data_list
        # Store the data(class object) list into a pickle file
        with open(pickle_path,'wb') as p:
            pickle.dump(data_lists, p)


if __name__ == '__main__':
    engine = SearchEngine()

    # Load data from corpus
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    local_filepath = './blogs/'
    pickle_path = './group_data_objects.pickle'
    if not os.path.isfile("group_data_objects.pickle"):
        engine.load_corpus(filepath, local_filepath, pickle_path)

    # input query
    while True:
        query = input()
        query_list, augment_obj = engine.process_query(query)
        # augment_obj. + synonyms_set, definition_set, hyponyms_set, hypernyms_set, antonyms_set, not_phrase_set, delete_set
        print(query_list, augment_obj.antonyms_set)
        # Compute simularity score

