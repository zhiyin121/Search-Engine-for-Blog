from get_data import GroupData, get_filename, get_data
from get_simularity import Score
from dp_similarity import SentenceTransformers

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import pandas as pd
import pickle

import nltk
# nltk.download('wordnet')
import numpy as np
import time

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


def main():
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
    print(' #5 Americam \t(Auto correct typo)')
    
    while True:
        print('\nWhat do you search for:')
        query = input()
        if query == "nothing":
            break
        else:
            # Compute simularity score
            print('\nLoading...')
            starting = time.time()

            query_score_dic, related_score_dic, all_score_dic = score.simularity_score(query)

            all_score_tuple = list(all_score_dic.items())
            all_score = np.array([i[1] for i in all_score_tuple])
            top_100_index = all_score.argpartition(-100)[-100:]
            #top_100 = sorted(all_score_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
            #print(top_100)
            top_100 = [all_score_tuple[i] for i in top_100_index]
            # Resort by vector similarity
            top_100 = sorted(top_100, key = lambda i: i[0])

            print('Ranking...')
            resort_dic = {}
            j = 0
            documents, ids = [], []
            for i in data_lists:
                doc_id = top_100[j][0]
                if i.blog_id == doc_id:
                    documents.append(i.post)
                    ids.append(i.blog_id)
                    j += 1
                    if j >= len(top_100):
                        break

            results = re_score.get_scores(query, documents)

            for id, sim in zip(ids, results):
                resort_dic[id] = sim.item()

            print('Ready to return results...')
            #print(resort_top_100)
            resort_dic_tuple = list(resort_dic.items())
            resort_score = np.array([i[1] for i in resort_dic_tuple])
            resort_top_100_index = resort_score.argsort()[::-1]
            #print(resort_top_100_index)
            resort_top_100 = [resort_dic_tuple[i] for i in resort_top_100_index]
            #print(resort_top_100)
            # resort_top_100 = sorted(resort_dic.items(),key=lambda item:item[1],reverse=True)[:100]  # [(blog_id, score)]
            df_dic = {
                'Score': [],
                'Post': [],
                'Date': [],
                'Blog ID': [],
                'User ID': [],
                'Gender': [],
                'Age': [],
                'Industry': [],
                'Astrology': [],
            }
            for doc in resort_top_100[:20]:
                doc_id = doc[0]
                sim_score = doc[1]
                for i in data_lists:
                    if i.blog_id == doc_id:
                        df_dic['Score'].append(sim_score)
                        df_dic['Post'].append(i.post)
                        df_dic['Date'].append(i.date)
                        df_dic['Blog ID'].append(i.blog_id)
                        df_dic['User ID'].append(i.user_id)
                        df_dic['Gender'].append(i.gender)
                        df_dic['Age'].append(i.age)
                        df_dic['Industry'].append(i.industry)
                        df_dic['Astrology'].append(i.astrology)
                        # print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')
            df = pd.DataFrame(data=df_dic)
            #df.sort_values(by=['Score'], inplace=True, ascending=False)
            ending = time.time()

            print("Running time: ", round(ending-starting, 3), "s\n")
            print(df)
            while True:
                print("\nWhich blog post would you like to see in full content? [number/n]")
                selection = input()
                if selection == 'n':
                    break
                else:
                    print("Full content of blog post ", selection, ':\n', df['Post'][int(selection)])



if __name__ == '__main__':
    main()