from get_data import GroupData, tokenizer

import json
import pickle
from collections import Counter
import spacy
import time
import string

spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
punct = set(string.punctuation)

# Get vocabuary dictionary from one text
def small_vocabuary(sentence):
    small_voc_dic = {}
    tokenizer_start_time = time.time()
    tokens = tokenizer(sentence)
    tokenizer_end_time = time.time()
    # print('tokenizer:', tokenizer_end_time-tokenizer_start_time)
    for token in tokens:
        if token not in spacy_stopwords and token not in punct:
            if token in small_voc_dic:
                small_voc_dic[token] += 1
            else:
                small_voc_dic[token] = 1
    return small_voc_dic


# Get vocabuary dictionary from the corpus
def vocabuary(data_lists):
    voc_dic = {}
    for i in data_lists:
        small_vocabuary_start_time = time.time()
        small_voc_dic = small_vocabuary(i.post)
        small_vocabuary_end_time = time.time()
        # print('small_vocabuary:', small_vocabuary_end_time-small_vocabuary_start_time)
        for voc,counts in small_voc_dic.items():
            if voc in voc_dic:
                voc_dic[voc] += counts
            else:
                voc_dic[voc] = counts
    with open("vocabuary_dictionary.json",'w') as v:
        json.dump(voc_dic,v)
    return voc_dic


# Get voc2id & id2voc dictionary
def voc_id(vocabuery):
    index = 0
    voc2id = {}; id2voc = {}
    for voc in vocabuary:
        voc2id[voc] = index
        id2voc[index] = voc
    return voc2id, id2voc


# Get inverted index
def get_indexing(data_lists, vocabuery):
    inverted_index = {}
    for i in data_lists:
        posting_list = []
        doc_token_number = 0
        sentences = i.post
        # Add document id as a list, to the dictionary of words it contains
        if voc2id[voc] in posting:
            posting[voc2id[voc]].append((i.blog_id, dic[voc], doc_token_number)) # {voc_id:[(blog_id_1, word count), ...]}
        else:
            posting[voc2id[voc]] = [(i.blog_id, dic[voc], doc_token_number)]
            
    
    
    with open("vocabuary_to_id.json",'w') as v2i:
        json.dump(voc2id,v2i)
    with open("id_to_vocabuary.json",'w') as i2v:
        json.dump(id2voc,i2v)
    with open("inverted_index.json",'w') as p:
        json.dump(posting,p)

    return


if __name__ == '__main__':
    # Read a pickle file
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)
    vocabuary_start_time = time.time()
    voc_dic = vocabuary(data_lists)
    vocabuary_end_time = time.time()
    print('vocabuary;', vocabuary_end_time-vocabuary_start_time)
    print('voc_dic: ', sorted(voc_dic.items(),key=lambda item:item[1],reverse=True)[:100])
    '''
    # Construct a vocabuary dictionary
    voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
    get_indexing(data_lists[:10], voc_dic, voc2id, id2voc, posting)
    # store voc_dic.json, voc2id.json, id2voc.json, posting.json
    
    # Print some samples
    
    print('id2voc: ', list(id2voc.items())[:10])
    print('voc2id: ', list(voc2id.items())[:10])
    print('posting: ', list(posting.items())[:10])'''
