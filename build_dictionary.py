from get_data import GroupData

import json
import pickle
from collections import Counter
import time
import string

import spacy
nlp = spacy.load("en_core_web_sm")
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
punct = set(string.punctuation)


regard_ent_type = ['LANGUAGE','DATE', 'TIME','MONEY','QUANTITY', 'ORDINAL', 'CARDINAL']
# Tokenize and lemmatize the sentence, while keeping the name entity phrase as an item
def tokenizer(text_list):
    token_list = []
    docs = nlp.pipe(text_list, disable=['tok2vec', 'parser'], n_process=30)
    for doc in docs:
        entities_atr = {}
        entities_phrase_dic = {}
        for ent in doc.ents:
            if ent.label_ not in regard_ent_type:
                entities_atr[ent.text] = ent.label_
                if ' ' in ent.text:
                    entities_phrase_dic[ent.text] = 0

        org_tokens_list = []
        for token in doc:
            org_tokens_list.append(token.text)
        #print(org_tokens_list)

        for index in range(len(org_tokens_list)):
            for name in entities_phrase_dic:
                if ' ' in name:
                    name_list = name.split(' ')
                else:
                    name_list = [name]
                if org_tokens_list[index:index+len(name_list)] == name_list:
                    #print(org_tokens_list[index:index+len(name_list)])
                    #print(name_list)
                    entities_phrase_dic[name] = (index, index + len(name_list))
        #print(entities_dic)

        with doc.retokenize() as retokenizer:
            for name in entities_phrase_dic:
                if entities_phrase_dic[name] != 0:
                    spans = doc[entities_phrase_dic[name][0]:entities_phrase_dic[name][1]]
                    #filtered = spacy.util.filter_spans(spans)
                    try:
                        retokenizer.merge(spans, attrs={"LEMMA": name.lower()})
                    except ValueError:
                        pass

        new_tokens_list = []
        for token in doc:
            if token.pos_ != 'SPACE':
                new_tokens_list.append(token.lemma_.lower()) # or token.text
        #print(new_tokens_list)
        token_list.append(new_tokens_list)

    return token_list #, entities_atr


# Get vocabuary dictionary from the corpus
def vocabuary(data_lists):
    voc_dic = {}
    text_list = [i.post for i in data_lists]
    doc = tokenizer(text_list)
    for tokens in doc:
        for token in tokens:
            if token not in spacy_stopwords and token not in punct:
                if token in voc_dic:
                    voc_dic[token] += 1
                else:
                    voc_dic[token] = 1
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
