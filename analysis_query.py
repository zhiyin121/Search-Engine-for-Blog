from get_data import GroupData

import pickle
from spellchecker import SpellChecker
spell = SpellChecker()

import spacy
nlp = spacy.load("en_core_web_sm")

import nltk
nltk.download('wordnet')
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

def enrich_query(query_list):
    synonyms_word = []
    related_word = []
    negation_word = []
    antonyms_list = []; not_phrase_list = []
    delete_set = set()

    for index in range(len(query_list)):
        token = query_list[index]
        # Related word
        if not nlp(token)[0].is_stop:
            t_synonyms_set, t_syn_definition_set = get_synonyms(token)
            related_word += list(t_syn_definition_set)
            synonyms_word += list(t_synonyms_set)
        # When it contains a negative expression
        ## not + adj/v -> ['not adj/v.'] or ['antonyms']
        ## not + n -> delete ['not v/n'] (not yet done)

        if token == 'not':
            next_token = query_list[index+1]
            # Compose phrases containing not
            not_phrase_list.append('not ' + next_token)
            synonyms_set, syn_definition_set = get_synonyms(next_token)
            for synonym in synonyms_set:
                not_phrase_list.append('not ' + synonym)
            # Remove 'not' and the words it modifies
            delete_set.add('not')
            delete_set.add(next_token)
            # Get the antonym of the word modified by 'not'
            antonyms_set, ant_definition_set = get_antonyms(next_token)
            if antonyms_set != set():
                antonyms_list += list(antonyms_set)

    negation_word = not_phrase_list + antonyms_list
    related_word += list(ant_definition_set)

    return synonyms_word, negation_word, related_word


def deal_negation(query):
    # not + adj -> ['not adj.'] or ['antonyms']
    return


def get_related():
    return

def get_hyponyms():
    return



if __name__ == '__main__':
    '''
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Print examples
    for i in data_lists[:2]:
        print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')'''

    query = 'I\'m not hapyy, but he doesn\'t know.'
    cleaned_query = clean_query(query)
    synonyms_word, negation_word, related_word = enrich_query(cleaned_query)
    print('cleaned_query:\n', cleaned_query, '\n',
    'synonyms_word:\n', synonyms_word, '\n',
    'negation_word:\n', negation_word, '\n',
    'related_word:\n', related_word)

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
