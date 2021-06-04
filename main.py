from get_data import GroupData, get_filename, get_data
from analysis_query import AugmentedQuery
from get_simularity import Score
from dp_similarity import SentenceTransformers

import os
import pickle

import nltk
nltk.download('wordnet')


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
            pickle.dump(data_lists, p)  # Size: 785.6M


if __name__ == '__main__':
    engine = SearchEngine()

    # Load data from corpus
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    local_filepath = './blogs/'
    pickle_path = './group_data_objects.pickle'
    if not os.path.isfile("group_data_objects.pickle"):
        engine.load_corpus(filepath, local_filepath, pickle_path)

    # input query
    print('Query example:\n')
    print(' #1 New York \t(Sensitive to named entities)')
    print(' #2 I\'m not happy \t(Understand adjective phrases modified by \'not\')')
    print(' #3 apple slow \t(Ambiguity)\n #4 apple pie \t(Ambiguity)\n')
    print('What do you search for:')

    re_score = SentenceTransformers()
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    while True:
        query = input()
        # Compute simularity score
        print('\nLodaing...')
        score = Score()
        query_score_dic, related_score_dic, all_score_dic = score.simularity_score(query)
        top_100 = sorted(all_score_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
        #print(top_100)
        # Resort by vector similarity
        
        print('Ranking...')
        resort_dic = {}
        for doc in top_100:
            doc_id = doc[0] 
            for i in data_lists:
                if i.blog_id == doc_id:
                    document = i.post
                    result = re_score.get_scores(query, document)
                    resort_dic[doc_id] = result
        #print(resort_top_100)
        print('Soon to return results...')
        resort_top_100 = sorted(resort_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
        for doc in resort_top_100[:10]:
            doc_id = doc[0]
            for i in data_lists:
                if i.blog_id == doc_id:
                    print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')
        
