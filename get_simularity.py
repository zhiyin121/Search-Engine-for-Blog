from get_data import GroupData
from build_dictionary import get_indexing
from analysis_query import clean_query, AugmentedQuery

import os
import json
import math
import pickle


class Score:
    def __init__(self):
        return

    def tf_idf(self, token_freq, doc_token_number, doc_with_token, doc_num):
        tf = token_freq/doc_token_number
        idf = math.log(doc_num/(doc_with_token+1))
        tf_idf = tf * idf
        return tf_idf

    def simularity_score(self, query, data_lists):
        # Processing query
        query_list = clean_query(query)
        augment = AugmentedQuery(query_list)
        augment_obj = augment.augment_query()
        # augment_obj. + synonyms_set, definition_set, hyponyms_set, 
        # augment_obj. + hypernyms_set, antonyms_set, not_phrase_set, delete_set
        
        # Construct a vocabuary dictionary
        if not os.path.isfile("vocabuary_dictionary.json"):
            voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
            get_indexing(data_lists, voc_dic, voc2id, id2voc, posting)
            # store voc_dic.json, voc2id.json, id2voc.json, posting.json

        with open("vocabuary_dictionary.json", 'r') as v:
            voc_dic = json.loads(v.read())
        with open("vocabuary_to_id.json", 'r') as v2i:
            voc2id = json.loads(v2i.read())
        with open("id_to_vocabuary.json", 'r') as i2v:
            id2voc = json.loads(i2v.read()) # Key is a string type integer
        with open("inverted_index.json", 'r') as p:
            posting = json.loads(p.read()) # Key is string type integer

        # Deleted 'not' phrase from query
        for token in augment_obj.delete_set:
            query_list.remove(token)
        # Add synonyms of 'not' phrase
            query_list += list(augment_obj.antonyms_set)
        # Obtain score by query token
        query_score_dic = {}
        doc_num = len(data_lists)
        for token in query_list:
            if token in voc2id:
                token_id = voc2id[token]
                doc_list = posting[str(token_id)]
                #print(doc_list)
                doc_with_token = len(doc_list)
                for info in doc_list:  #[(doc id, token freq, doc token number), ...]
                    doc_id = info[0]
                    token_freq = info[1]
                    doc_token_number  = info[2]
                    tf_idf_score = self.tf_idf(token_freq, doc_token_number, doc_with_token, doc_num)
                    if doc_id in query_score_dic:
                        query_score_dic[doc_id] += tf_idf_score
                    else:
                        query_score_dic[doc_id] = tf_idf_score

        # Obtain score by related word
        related_score_dic = {}
        related_token = list(augment_obj.synonyms_set | augment_obj.definition_set | augment_obj.hyponyms_set | augment_obj.hypernyms_set)
        for token in related_token:
            if token in voc2id:
                token_id = voc2id[token]
                doc_list = posting[str(token_id)]
                for info in doc_list:  #[(doc id, token freq, doc token number), ...]
                    doc_id = info[0]
                    if doc_id in related_score_dic:
                        related_score_dic[doc_id] += 1
                    else:
                        related_score_dic[doc_id] = 1

        return query_score_dic, related_score_dic


if __name__ == '__main__':
    # Load data from corpus
    filepath = '/Users/tan/OneDrive - xiaozhubaoxian/blog/blogs/'
    local_filepath = './blogs/'
    pickle_path = './group_data_objects.pickle'
    if not os.path.isfile("group_data_objects.pickle"):
        engine.load_corpus(filepath, local_filepath, pickle_path)

    # Read a pickle file
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    query = 'hate exam'
    score = Score()
    query_score_dic, related_score_dic = score.simularity_score(query, data_lists[:20])
    query_score_dic_20 = sorted(query_score_dic.items(),key=lambda item:item[1],reverse=True)[:100]
    related_score_dic_20 = sorted(related_score_dic.items(),key=lambda item:item[1],reverse=True)[:100]
    print('query_score_dic:\n', query_score_dic_20)
    print('related_score_dic:\n', related_score_dic_20)
    
    inter = []
    for i in query_score_dic_20:
        for j in related_score_dic_20:
            if i[0] == j[0]:
                inter.append(i[0])
    print(inter)

    '''
    query = 'I\'m not hapyy'
    tokens = clean_query(query)
    doc_dic = {}
    for token in tokens:
        doc_list = posting[voc2id[token]]
        for doc in doc_list:
            if doc[0] not in doc_dic:
                doc_dic[doc[0]] = 1
            else:
                doc_dic[doc[0]] += 1
    
    doc_list = sorted(doc_dic.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    print(doc_list[:20])
    for tup in doc_list[:20]:
        index = tup[0]
        print(index)
        for i in data_lists:
            if i.blog_id == index:
                print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')'''
