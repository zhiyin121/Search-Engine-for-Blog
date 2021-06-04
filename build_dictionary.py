from get_data import GroupData

import json
import pickle
from collections import Counter
import time
import string
import os

import spacy
nlp = spacy.load("en_core_web_sm")
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS
punct = set(string.punctuation)


regard_ent_type = ['LANGUAGE','DATE', 'TIME','MONEY','QUANTITY', 'ORDINAL', 'CARDINAL']
# Tokenize and lemmatize the sentence, while keeping the name entity phrase as an item
def tokenizer(text_list, as_tuple=False):
    token_list = []
    if not as_tuple:
        docs = nlp.pipe(text_list, disable=['tok2vec', 'parser'], n_process=2)
    else:
        from spacy.tokens import Doc
        if not Doc.has_extension("text_id"):
            Doc.set_extension("text_id", default=None)
        doc_tuples = nlp.pipe(text_list, disable=['tok2vec', 'parser'], n_process=127, as_tuples=True, batch_size=3000)
        docs = []
        for doc, context in doc_tuples:
            print(context["blog_id"], len(text_list))
            doc._.text_id = context["blog_id"]
            docs.append(doc)
    i = 0
    for doc in docs:
        print(i, len(text_list))
        i += 1
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
        if as_tuple:
            new_tokens_list.append(doc._.text_id)
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
def voc_id(vocabuary):
    index = 0
    voc2id = {'<unk>': -1}; id2voc = {}
    for voc in vocabuary:
        voc2id[voc] = index
        id2voc[index] = voc
        index += 1
    return voc2id, id2voc
            

def get_posting_list(docs, vocabuary_to_id):
    indexing = {}
    i = 0
    for tokens in docs:
        print(i, len(docs))
        i += 1
        blog_id = tokens[-1]
        count = Counter(tokens[:-1])
        for token in count:
            freq = count[token]
            if token in vocabuary_to_id:
                voc_id = vocabuary_to_id[token]
                if voc_id in indexing:
                    indexing[voc_id].append((blog_id, freq))
                else:
                    indexing[voc_id] = [(blog_id, freq)]
    return indexing


def build():
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    if not os.path.isfile("voc_dic.pkl"):
        voc_dic = vocabuary(data_lists)
        with open('voc_dic.pkl','wb') as file:
            pickle.dump(voc_dic, file)
    else:
        voc_dic = pickle.load(open('voc_dic.pkl', 'rb'))
    #print('vocabuary;', vocabuary_end_time-vocabuary_start_time)
    #print('voc_dic: ', sorted(voc_dic.items(),key=lambda item:item[1],reverse=True)[:100])

    # Construct a vocabuary dictionary
    
    if not os.path.isfile("voc2id.pickle"):
        voc2id, id2voc = voc_id(voc_dic)
        with open('voc2id.pickle','wb') as file:
            pickle.dump(voc2id, file)
        with open('id2voc.pickle','wb') as file:
            pickle.dump(id2voc, file)
    else:
        voc2id = pickle.load(open('voc2id.pickle', 'rb'))
        id2voc = pickle.load(open('id2voc.pickle', 'rb'))
    #print('id2voc: ', list(id2voc.items())[:10])
    #print('voc2id: ', list(voc2id.items())[:10])
    
    # store voc_dic.json, voc2id.json, id2voc.json, posting.json
    if not os.path.isfile("posting_list.pickle"):
        text_list = [(i.post, {'blog_id': i.blog_id}) for i in data_lists]
        tokens = tokenizer(text_list, as_tuple=True)
        with open('tokens.pickle','wb') as file:
            pickle.dump(tokens, file)
        posting_list = get_posting_list(tokens, voc2id)
    # Print some samples
        print('posting: ', list(posting_list.items())[:10])
        with open('posting_list.pickle','wb') as file:
            pickle.dump(posting_list, file)
    else:
        posting_list = pickle.load(open('posting_list.pickle', 'rb'))


if __name__ == '__main__':
    # Read a pickle file
    build()
