from get_data import GroupData

import pickle
from collections import Counter
import spacy
nlp = spacy.load("en_core_web_sm")
lemmatizer = nlp.get_pipe("lemmatizer")

def get_small_vocabuary(paragraph):
    voc_dic = {}
    doc = nlp(paragraph)
    for token in doc:
        lemma = token.lemma_.lower() # Lemalization and lower case
        if lemma in voc_dic:
            voc_dic[lemma] += 1
        else:
            voc_dic[lemma] = 1
    return voc_dic


def get_indexing(data_lists, voc_dic, voc2id, id2voc, posting):
    for i in data_lists:
        dic = get_small_vocabuary(i.post)
        for voc in dic:
            # Construct a vocabuary dictionary
            if voc in voc_dic:
                voc_dic[voc] += dic[voc] # {voc:word counts}
            else:
                voc_dic[voc] = dic[voc]

            # Get two vocbuary id dictionaries
            if voc in voc2id:
                pass
            else:
                index = max(voc2id.values()) + 1
                voc2id[voc] = index # {voc:voc_id}
                id2voc[index] = voc # {voc_id:voc}

            # Add document id as a list, to the dictionary of words it contains
            if voc2id[voc] in posting:
                posting[voc2id[voc]].append((i.blog_id, dic[voc])) # {voc_id:[(blog_id_1, word count), ...]}
            else:
                posting[voc2id[voc]] = [(i.blog_id, dic[voc])]
    return voc_dic, voc2id, id2voc, posting


if __name__ == '__main__':
    # Read a pickle file
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Construct a vocabuary dictionary
    voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
    voc_dic, voc2id, id2voc, posting = get_indexing(data_lists[:100], voc_dic, voc2id, id2voc, posting)
    del voc2id['unk']

    # Print some samples
    print('voc_dic: ', list(voc_dic.items())[:10])
    print('id2voc: ', list(id2voc.items())[:10])
    print('voc2id: ', list(voc2id.items())[:10])
    print('posting: ', list(posting.items())[:10])
<<<<<<< HEAD

=======
>>>>>>> origin/master
