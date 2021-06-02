from get_data import GroupData, get_filename, clean_data, get_data
from build_dictionary import get_indexing
from analysis_query import clean_query, AugmentedQuery

<<<<<<< HEAD
import os
=======
>>>>>>> c9b7dcb3019ba9f69ab5ade1ff9a18b2be84c76d
import pickle


class SearchEngine:
    def __init__(self):
        return
        
    def process_query(self, query):
        query_list = clean_query(query)
        augment = AugmentedQuery(query_list)
        augment_obj = augment.augment_query()
        return query_list, augment_obj

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

    def build_dictionary(self, pickle_path):
        # Read a pickle file
        with open(pickle_path, 'rb') as f:
            data_lists = pickle.load(f)
        # Construct a vocabuary dictionary
        voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
        voc_dic, voc2id, id2voc, posting = get_indexing(data_lists[:100], voc_dic, voc2id, id2voc, posting)
        del voc2id['unk']    


if __name__ == '__main__':
    engine = SearchEngine()
    # Load data from corpus
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    local_filepath = './blogs/'
    pickle_path = './group_data_objects.pickle'
    if not os.path.isfile("group_data_objects.pickle"):
        engine.load_corpus(filepath, local_filepath, pickle_path)
    engine.build_dictionary(pickle_path)
    # Processing query
    query = 'who like cute cats?'
    query_list, augment_obj = engine.process_query(query)
    print(query_list, augment_obj.antonyms_set)
    # Compute simularity score

