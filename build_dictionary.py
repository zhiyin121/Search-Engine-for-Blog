from get_data import GroupData

import json
import pickle
from collections import Counter
import spacy

nlp = spacy.load("en_core_web_sm")
lemmatizer = nlp.get_pipe("lemmatizer")

def get_small_vocabuary(paragraph):
    voc_dic = {}
    doc = nlp(paragraph)
    doc_token_number = 0
    for token in doc:
        # Lemalization and lower case
        lemma = token.lemma_.lower()
        if lemma in voc_dic:
            voc_dic[lemma] += 1
        else:
            voc_dic[lemma] = 1
        doc_token_number += 1
    return voc_dic, doc_token_number


# Get vocabuary dictionary, voc2id & id2voc dictionary, and posting list
def get_indexing(data_lists, voc_dic, voc2id, id2voc, posting):
    for i in data_lists:
        dic, doc_token_number = get_small_vocabuary(i.post)
        for voc in dic:
            # Construct a vocabuary dictionary
            if voc in voc_dic:
                voc_dic[voc] += dic[voc] # {voc:word counts}
            else:
                voc_dic[voc] = dic[voc]
            with open("vocabuary_dictionary.json",'w') as v:
                json.dump(voc_dic,v)

            # Get two vocbuary id dictionaries
            if voc not in voc2id:
                index = max(voc2id.values()) + 1
                voc2id[voc] = index # {voc:voc_id}
                id2voc[index] = voc # {voc_id:voc}
            with open("vocabuary_to_id.json",'w') as v2i:
                json.dump(voc2id,v2i)
            with open("id_to_vocabuary.json",'w') as i2v:
                json.dump(id2voc,i2v)

            # Add document id as a list, to the dictionary of words it contains
            if voc2id[voc] in posting:
                posting[voc2id[voc]].append((i.blog_id, dic[voc], doc_token_number)) # {voc_id:[(blog_id_1, word count), ...]}
            else:
                posting[voc2id[voc]] = [(i.blog_id, dic[voc], doc_token_number)]
            with open("inverted_index.json",'w') as p:
                json.dump(posting,p)
    return


if __name__ == '__main__':
    # Read a pickle file
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Construct a vocabuary dictionary
    voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
    get_indexing(data_lists[:10], voc_dic, voc2id, id2voc, posting)
    # store voc_dic.json, voc2id.json, id2voc.json, posting.json
    
    # Print some samples
    print('voc_dic: ', list(voc_dic.items())[:10])
    print('id2voc: ', list(id2voc.items())[:10])
    print('voc2id: ', list(voc2id.items())[:10])
    print('posting: ', list(posting.items())[:10])
