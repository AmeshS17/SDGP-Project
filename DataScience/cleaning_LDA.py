import numpy as np
import pandas as pd
import json
import spacy
import sys

import bbcode
import re

from spacy_langdetect import LanguageDetector
from gensim.parsing.preprocessing import STOPWORDS

import gensim

parser = bbcode.Parser()

with open('./en_contractions/contra_dict.txt') as contra_dict:
    cList = json.load(contra_dict)

c_re = re.compile('(%s)' % '|'.join(cList.keys()))


def expandContractions(text, c_re=c_re):
    def replace(match):
        return cList[match.group(0)]

    return c_re.sub(replace, text.lower())


Number_dict = {'0': 'zero',
               '1': 'one',
               '2': 'two',
               '3': 'three',
               'ii': 'two',
               'iii': 'three'
               }


# number to word
def num2word(d):
    if (len(d) == 1 and d in '0123') or (d in ['ii', 'iii']):
        word = Number_dict[d]

    elif len(str(d)) == 1 and str(d) in '0123':
        word = Number_dict(str(d))

    else:
        word = d

    return word


english_stopwords = list(set(STOPWORDS))


# removing english stopwords
def remove_stopwords(doc):
    words = [num2word(w) for w in doc if w != '' and w not in english_stopwords]
    return words


# combine cleaning functions into one function
def parse_clean(text):
    parsed_text = parser.strip(text)  # remove BBcode notations from text

    text = expandContractions(parsed_text)  # expand contractions; return all text in lower case

    text = re.split(r'\W+', text)  # separate words from punctuation (e.g. remove "'s" from "Cao Cao's")

    text = [num2word(w) for w in text]  # convert single digits to words before word len check, or they will be lost

    # All word lengths should be >1 character and <= length of the longest word in the English language. It's common
    # for people spam incoherent letters on the Internet.
    text = [word for word in text if word not in english_stopwords and 1 < len(word) <= len(
        'pneumonoultramicroscopicsilicovolcanoconiosis')]

    clean_text = [num2word(w) for w in text]

    return clean_text


# tokenizing and removing stopwords
def stop_clean(texts):
    texts = [parse_clean(doc) for doc in texts]
    texts = [remove_stopwords(doc) for doc in texts]

    return texts


# spacy lemma with allowed postags
def spacy_lemma(bow, allowed_postags=['NOUN']):
    lemma_doc = nlp(" ".join(bow))

    lemma_text = [token.text if '_' in token.text else token.lemma_ if token.pos_ in allowed_postags else '' for token
                  in lemma_doc]

    return lemma_text


# read the json
with open(sys.argv[1]) as json_file:
    jayson = json.load(json_file)

# making a list from the json which contains reviews
review_data = [v for v in jayson['reviews'].values()]

# making dict from json
steam_reviews_dict = {'recommendationid': [review_data[i]['recommendationid'] for i in range(len(review_data))],

                      'author_steamid': [review_data[i]['author']['steamid'] for i in range(len(review_data))],

                      'author_num_games_owned': [review_data[i]['author']['num_games_owned'] for i in
                                                 range(len(review_data))],

                      'author_num_reviews': [review_data[i]['author']['num_reviews'] for i in range(len(review_data))],

                      'author_playtime_forever': [review_data[i]['author']['playtime_forever'] for i in
                                                  range(len(review_data))],

                      'author_playtime_last_two_weeks': [review_data[i]['author']['playtime_last_two_weeks'] for i in
                                                         range(len(review_data))],

                      'author_last_played': [review_data[i]['author']['last_played'] for i in range(len(review_data))],

                      'review': [review_data[i]['review'] for i in range(len(review_data))],

                      'timestamp_created': [review_data[i]['timestamp_created'] for i in range(len(review_data))],

                      'timestamp_updated': [review_data[i]['timestamp_updated'] for i in range(len(review_data))],

                      'voted_up': [review_data[i]['voted_up'] for i in range(len(review_data))],

                      'weighted_vote_score': [review_data[i]['weighted_vote_score'] for i in range(len(review_data))],

                      'steam_purchase': [review_data[i]['steam_purchase'] for i in range(len(review_data))],

                      'received_for_free': [review_data[i]['received_for_free'] for i in range(len(review_data))],

                      'written_during_early_access': [review_data[i]['written_during_early_access'] for i in
                                                      range(len(review_data))]}
# making a dataframe using the dict
data_frame_raw = pd.DataFrame(steam_reviews_dict)

