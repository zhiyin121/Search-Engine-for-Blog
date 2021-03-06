from build_dictionary import tokenizer
from get_data import GroupData

from itertools import product
from spellchecker import SpellChecker
spell = SpellChecker()

import spacy
nlp = spacy.load("en_core_web_sm")

from nltk.corpus import wordnet
# from gensim.models import KeyedVectors
# from negspacy.negation import Negex # negate name entity
spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

def spelling_correction(query_list):
    corrected_query = []
    # Spelling correction: Yes or No?
    for token in query_list:
        correct = spell.correction(token)
        if correct:
            corrected_query.append(correct)
        else:
            corrected_query.append(token)
    if query_list != corrected_query:
        print('Do you mean "' + ' '.join(corrected_query) + '"?')
        chose = input("Yes, No, or Additional options required? [y/n/a]\n")
        if chose == 'y':
            return corrected_query
        elif chose == 'n':
            print("Remind: this may cause no results returned.")
            return query_list
        elif chose == 'a':
            candidate_token_list = []
            candidates_list = []
            for token in query_list:
                token_candidate = []
                correct = spell.candidates(token)
                if correct:
                    token_candidate = correct
                else:
                    token_candidate.append(token)
                candidate_token_list.append(token_candidate)
            for i in product(*candidate_token_list):
                candidates_list.append(list(i))
            index = 0
            candidates_dic = {}
            for c in candidates_list:
                candidates_dic[index] = c
                index += 1
            print(candidates_dic)
            chose_add = input("choose one candidates or keep the original? [number/o]\n")
            if chose_add == 'o':
                return query_list
            else:
                return candidates_dic[int(chose_add)]
    else:
        return query_list
    
#print(spelling_correction(['childrem']))

class AugmentSet:
    def __init__(self,synonyms_set, definition_set, hyponyms_set, hypernyms_set, antonyms_set, not_phrase_set, delete_set):
        self.synonyms_set = synonyms_set
        self.definition_set = definition_set
        self.hyponyms_set = hyponyms_set
        self.hypernyms_set = hypernyms_set
        self.antonyms_set = antonyms_set
        self.not_phrase_set = not_phrase_set
        self.delete_set = delete_set

class AugmentedQuery:
    def __init__(self, query_list):
        self.query_list = query_list
        #self.wiki = KeyedVectors.load_word2vec_format(wiki_path, limit=999999)
        

    # Get synonyms set of a word from the corpus WordNet
    def get_synonyms(self, word):
        #sym = self.model.most_similar_cosmul(positive=tokens, negative=not tokens, topn=5)
        if ' ' in word:
            word = word.replace(' ', '_') # Able to handle phrases
        synonyms_set = set()
        definition_set = set()
        syns = wordnet.synsets(word)
        #print(syns)
        for token in syns:
            # Get synonyms
            syn = token.lemma_names()
            #print(syn)
            for s in syn:
                if '_' in s:
                    s = s.replace('_', ' ')
                synonyms_set.add(s)
            # Get related word via definition
            definition = token.definition().split(' ')
            for word in definition:
                word = nlp(word)[0].lemma_.lower()
                if word not in spacy_stopwords:
                    definition_set.add(word)
        return synonyms_set, definition_set

    # Get antonyms set of a word if available from the corpus WordNet
    def get_antonyms(self, word):
        if ' ' in word:
            word = word.replace(' ', '_') # Able to handle phrases
        antonyms_set = set()
        definition_set = set()
        syns = wordnet.synsets(word)
        #print(syns)
        for token in syns:
            #print(token.lemmas()[0])
            #print(token.lemmas()[0].antonyms())
            if token.lemmas()[0].antonyms():
                # Get antonyms
                ant = [token.lemmas()[0].antonyms()[0].name()]
                for a in ant:
                    antonyms_set.add(a)
                # Get related word via definition
                definition = token.lemmas()[0].antonyms()[0].synset().definition().split(' ')
                for word in definition:
                    word = nlp(word)[0].lemma_.lower()
                    if word not in spacy_stopwords:
                        definition_set.add(word)
        return antonyms_set, definition_set # Could be empty set()

    # Get hyponyms set of a word if available from the corpus WordNet
    # P.S. some of the output is somewhat old fashioned, e.g. 'phone' -> 'pay station'
    def get_hyponyms(self, word):
        if ' ' in word:
            word = word.replace(' ', '_') # Able to handle phrases
        hyponyms_set = set()
        syns = wordnet.synsets(word)
        for token in syns:
            hyps = token.hyponyms()
            for hyp in hyps:
                hyponyms_list = hyp.lemma_names()
                for hyponym in hyponyms_list:
                    if '_' in hyponym:
                        hyponym = hyponym.replace('_', ' ')
                    hyponyms_set.add(hyponym)
        return hyponyms_set # Could be empty set()

    # Get hypernyms set of a word if available from the corpus WordNet
    def get_hypernyms(self, word):
        if ' ' in word:
            word = word.replace(' ', '_') # Able to handle phrases
        hypernyms_set = set()
        syns = wordnet.synsets(word)
        for token in syns:
            hyps = token.hypernyms()
            for hyp in hyps:
                hypernyms_list = hyp.lemma_names()
                for hypernym in hypernyms_list:
                    if '_' in hypernym:
                        hypernym = hypernym.replace('_', ' ')
                    hypernyms_set.add(hypernym)
        return hypernyms_set # Could be empty set()

    def get_negation(self, query_list):
        antonyms_set = set()
        delete_set = set()
        not_phrase_set = set()
        for index in range(len(query_list)):
            token = query_list[index]
            # When it contains a negative expression
            ## not + adj/v -> ['not adj/v.'] or ['antonyms']
            ## not + n -> delete ['not v/n'] (not yet done)
            if token == 'not' or token == 'n\'t':
                next_token = query_list[index+1]
                # Compose phrases containing not (semantically related)
                # Bonus points if the document is included, no reduction if it is not
                not_phrase_set.add('not ' + next_token)
                synonyms_set, syn_definition_set = self.get_synonyms(next_token)
                for synonym in synonyms_set:
                    not_phrase_set.add('not ' + synonym)
                # Remove 'not' and the words it modifies
                delete_set.add('not')
                delete_set.add(next_token)
                # Get the antonym of the word modified by 'not'
                antonyms_set, ant_definition_set = self.get_antonyms(next_token)
        return antonyms_set, not_phrase_set, delete_set

    # Get related enterty or properties (KG)
    def get_related():
        return

    def augment_query(self):
        # Get the phrase containing 'not' and discover the semantically similar word
        antonyms_set, not_phrase_set, delete_set = self.get_negation(self.query_list)

        # Get each word(except stopwords)'s synonyms, hyponyms, and hypernyms 
        synonyms_set = set(); definition_set = set(); hyponyms_set = set(); hypernyms_set = set()

        for index in range(len(self.query_list)):
            token = self.query_list[index]
            if token not in spacy_stopwords:
                if token not in delete_set:
                    synonyms, definition = self.get_synonyms(token)
                    synonyms_set = synonyms_set | synonyms
                    definition_set = definition_set | definition

                    hyponyms_set = hyponyms_set | self.get_hyponyms(token)
                    hypernyms_set = hypernyms_set | self.get_hypernyms(token)

        augment_obj = AugmentSet(synonyms_set, definition_set, hyponyms_set, hypernyms_set, antonyms_set, not_phrase_set, delete_set)
        return augment_obj


if __name__ == '__main__':
    '''
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Print examples
    for i in data_lists[:2]:
        print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')'''

    
    #query = ['I\'m not hapyy, but he doesn\'t know.']
    query = ['cat is not happy in New York']
    tokenized_query = tokenizer(query)[0]
    print(tokenized_query)
    e = AugmentedQuery(tokenized_query)
    augment_obj = e.augment_query()
    print(augment_obj.hyponyms_set)
    print(augment_obj.hypernyms_set)
    

    
    
