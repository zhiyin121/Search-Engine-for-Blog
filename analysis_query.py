from get_data import GroupData

import pickle
from spellchecker import SpellChecker
spell = SpellChecker()

import spacy
nlp = spacy.load("en_core_web_sm")


def clean_query(query):
    # Lemalization and lower case
    cleaned_query = []
    doc = nlp(query)
    for token in doc:
        lemma = token.lemma_.lower()
        # Spelling correction
        correct = spell.correction(lemma)
        if correct:
            cleaned_query.append(correct)
        else:
            cleaned_query.append(lemma)
    return cleaned_query


def get_synonym():
    return


def get_related():
    return



if __name__ == '__main__':
    with open('./group_data_objects.pickle', 'rb') as f:
        data_lists = pickle.load(f)

    # Print examples
    for i in data_lists[:2]:
        print(i.blog_id, i.user_id, i.gender, i.age, i.industry, i.astrology, i.date, i.post, '\n')

    query = 'I\'m not hapyy'
    voc = clean_query(query)
    print(voc)
    post_num = 0
    for i in data_lists:
        n = 0
        for word in voc:
            if word in i.post:
                n += 1
        if n == len(voc):
            post_num += 1
    print(post_num)
