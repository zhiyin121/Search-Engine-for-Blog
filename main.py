from get_data import GroupData, get_filename, get_data
from get_simularity import Score
from dp_similarity import SentenceTransformers

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import pickle

import nltk
# nltk.download('wordnet')
import numpy as np

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

    re_score = SentenceTransformers()
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)
    score = Score()
    # input query
    print('Query example:\n')
    print(' #1 New York \t(Sensitive to named entities)')
    print(' #2 I\'m not happy \t(Understand adjective phrases modified by \'not\')')
    print(' #3 apple slow \t(Ambiguity)\n #4 apple pie \t(Ambiguity)')
    print(' #5 Americam \t(Auto correct typo)\n')
    
    while True:
        print('What do you search for:')
        query = input()
        # Compute simularity score
        print('\nLoading...')
        
        query_score_dic, related_score_dic, all_score_dic = score.simularity_score(query)

        all_score_tuple = list(all_score_dic.items())
        all_score = np.array([i[1] for i in all_score_tuple])
        top_100_index = all_score.argpartition(-100)[-100:]
        #top_100 = sorted(all_score_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
        #print(top_100)
        top_100 = [all_score_tuple[i] for i in top_100_index]
        # Resort by vector similarity
        
        print('Ranking...')
        round = 0
        resort_dic = {}
        for doc in top_100:
            doc_id = doc[0] 
            for i in data_lists:
                if i.blog_id == doc_id:
                    document = i.post
                    result = re_score.get_scores(query, document)
                    resort_dic[doc_id] = result
            round += 1
            if round == len(top_100)/2:
                print('Ready to return results...\n')
        #print(resort_top_100)
        resort_dic_tuple = list(resort_dic.items())
        resort_score = np.array([i[1] for i in resort_dic_tuple])
        resort_top_100_index = resort_score.argpartition(-100)[-100:]
        resort_top_100 = [all_score_tuple[i] for i in resort_top_100_index]
        # resort_top_100 = sorted(resort_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
        # print(resort_top_100)
        for doc in resort_top_100[:7]:
            doc_id = doc[0]
            score = doc[1]
            for i in data_lists:
                if i.blog_id == doc_id:
                    print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, score, '\n')
        
