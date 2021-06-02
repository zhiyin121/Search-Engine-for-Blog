from get_data import GroupData

import pickle
from spellchecker import SpellChecker
spell = SpellChecker()

import spacy
nlp = spacy.load("en_core_web_sm")

import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet

from negspacy.negation import Negex # negate name entity


# Get synonyms list of a word from the corpus WordNet
def get_synonyms(word):
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
            if not nlp(word)[0].is_stop:
                definition_set.add(word)
    return synonyms_set, definition_set


# Get antonyms list of a word if available from the corpus WordNet
def get_antonyms(word):
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
                if not nlp(word)[0].is_stop:
                    definition_set.add(word)
    return antonyms_set, definition_set


def clean_query(query):
    # Lemalization and lower case
    cleaned_query = []
    pos_list = []
    doc = nlp(query)
    for token in doc:
        # Get the corresponding lemma and POS
        lemma = token.lemma_.lower()
        pos_list.append(token.pos_)
        # Spelling correction
        correct = spell.correction(lemma)
        if correct:
            cleaned_query.append(correct)
        else:
            cleaned_query.append(lemma)
    return cleaned_query


def get_negation(query_list):
    delete_set = set()
    not_phrase_set = set()
    for index in range(len(query_list)):
        token = query_list[index]
        # When it contains a negative expression
        ## not + adj/v -> ['not adj/v.'] or ['antonyms']
        ## not + n -> delete ['not v/n'] (not yet done)
        if token == 'not':
            next_token = query_list[index+1]
            # Compose phrases containing not (semantically related)
            # Bonus points if the document is included, no reduction if it is not
            not_phrase_set.add('not ' + next_token)
            synonyms_set, syn_definition_set = get_synonyms(next_token)
            for synonym in synonyms_set:
                not_phrase_set.add('not ' + synonym)
            # Remove 'not' and the words it modifies
            delete_set.add('not')
            delete_set.add(next_token)
            # Get the antonym of the word modified by 'not'
            antonyms_set, ant_definition_set = get_antonyms(next_token)
    return antonyms_set, not_phrase_set, delete_set



def get_hyponyms():
    return

# Get related enterty or properties (KG)
def get_related():
    return


def enrich_query(query_list):
    # Get the phrase containing 'not' and discover the semantically similar word
    antonyms_set, not_phrase_set, delete_set = get_negation(query_list)
    
    # Get each word's synonym except stopwords
    synonyms_set = set(); definition_set = set()
    for index in range(len(query_list)):
        token = query_list[index]
        if not nlp(token)[0].is_stop:
            synonyms, definition = get_synonyms(token)
            synonyms_set = synonyms_set | synonyms
            definition_set = definition_set | definition
    return antonyms_set, not_phrase_set, delete_set, synonyms_set, definition_set


if __name__ == '__main__':
    '''
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Print examples
    for i in data_lists[:2]:
        print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')'''

    query = 'I\'m not hapyy, but he doesn\'t know.'
    cleaned_query = clean_query(query)
    antonyms_set, not_phrase_set, delete_set, synonyms_set, definition_set = enrich_query(cleaned_query)

    print('cleaned_query:\n', cleaned_query, '\n',
    'synonyms_set:\n', synonyms_set, '\n',
    'antonyms_set:\n', antonyms_set, '\n',
    'definition_set:\n', definition_set, '\n',
    'not_phrase_set:\n', not_phrase_set, '\n',
    'delete_set:\n', delete_set)

    #print(get_synonyms('know'))

    '''
    post_num = 0
    for i in data_lists:
        n = 0
        for word in tokens:
            if word in i.post:
                n += 1
        if n == len(tokens):
            post_num += 1
    print(post_num)'''
