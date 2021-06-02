from get_data import GroupData
from build_dictionary import get_indexing
from analysis_query import clean_query, AugmentedQuery

import math
import pickle


class Dictionary:
    def __init__(self, voc_dic, voc2id, id2voc, posting):
        self.voc_dic = voc_dic
        self.voc2id = voc2id
        self.id2voc = id2voc
        self.posting = posting
        return
    
    def get_dic(self, data_lists):
        self.voc_dic, self.voc2id,\
        self.id2voc, self.posting = get_indexing(data_lists,\
                                    self.voc_dic, self.voc2id,\
                                    self.id2voc, self.posting)
        if self.voc2id['unk']:
            del self.voc2id['unk']


class Score:
    def __init__(self, query, document):
        self.query = query
        self.document = document
        return

    def simularity_score(self, query, data_lists):
        # Processing query
        query_list = clean_query(query)
        augment = AugmentedQuery(query_list)
        augment_obj = augment.augment_query()
        # augment_obj. + synonyms_set, definition_set, hyponyms_set, 
        # augment_obj. + hypernyms_set, antonyms_set, not_phrase_set, delete_set
        
        # Construct a vocabuary dictionary
        voc_dic = {}; voc2id = {'unk': -1}; id2voc = {}; posting = {}
        dic_obj = Dictionary(voc_dic, voc2id, id2voc, posting)
        dic_obj.get_dic(data_lists[:10])
        # dic_obj. + voc_dic, voc2id, id2voc, posting

        score_dic = {}
        doc_num = len(data_lists)
        voc_num = len(voc2id)
        for token in query_list:
            if token in voc2id:
                token_id = voc2id[token]
                doc_list = posting[token_id]
                for info in doc_list:  #[(doc id, token freq, doc token number), ...]
                    doc_id = info[0]
                    token_freq = info[1]
                    doc_token_number  = info[2]
                    doc_with_token = len(doc_list)
                    tf = token_freq/doc_token_number
                    idf = math.log((doc_with_token+1)/(doc_num+voc_num))
                    tf_idf = tf * idf
                    if doc_id in score_dic:
                        score_dic[doc_id] += tf_idf
                    else:
                        score_dic[doc_id] = tf_idf
        return 


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
