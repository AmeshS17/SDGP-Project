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


data_frame_raw = data_frame_raw[data_frame_raw['received_for_free'] == False]

data_frame_raw['author_playtime_forever'] = data_frame_raw['author_playtime_forever'] / 60

data_frame_raw['author_playtime_last_two_weeks'] = data_frame_raw['author_playtime_last_two_weeks'] / 60

data_frame_raw['review_length'] = data_frame_raw['review'].map(lambda x: len(x.split()))

data_frame_raw_num = data_frame_raw.select_dtypes(exclude=['O', 'bool'])

# at least 8 hours of minimum playtime
dataframe_usable = data_frame_raw[
    (data_frame_raw['author_playtime_forever'] >= 8)]

dataframe_usable['review_length'] = dataframe_usable['review'].map(lambda x: len(x.split()))

# setting percentile to 40% to get rid of overly short reviews

dataframe_ready = dataframe_usable[dataframe_usable['review_length'] > np.percentile(dataframe_usable['review_length'], 40)].reset_index(drop=True)

dataframe_cleaning = dataframe_ready.drop_duplicates(subset=['author_steamid', 'review'])

# get languages by document
from spacy.language import Language


# create custom component to use add pipe
@Language.factory("my_component")
def my_component(nlp, name):
    return LanguageDetector()


# get languages by document
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("my_component", last=True)


def get_document_language(text):
    doc = nlp(text)
    return doc._.language['language']


doc_langs = [get_document_language(x) for x in dataframe_cleaning['review']]
dataframe_cleaning['review_lang'] = doc_langs

dataframe_languages_cleaned = dataframe_cleaning[dataframe_cleaning['review_lang'] == 'en'].reset_index(drop=True)

model_dataframe = dataframe_languages_cleaned[['timestamp_created', 'review']]

model_dataframe['clean_reviews'] = stop_clean(model_dataframe['review'])

model_dataframe['clean_reviews'] = model_dataframe['clean_reviews'].map(lambda x: remove_stopwords(x))

# Build the bigram and trigram models
#The bigram and trigram modeks are getting built here
# feed a list of lists of words e.g. [['word1','word2'],['word3',# 'word4'] to get bigrams]
bigram_model = gensim.models.Phrases(list(model_dataframe['clean_reviews']), min_count=5,threshold=10)

#The trigram model is getting built here
trigram_model = gensim.models.Phrases(bigram_model[list(model_dataframe['clean_reviews'])], threshold=10)

# Faster way to get a sentence clubbed as a trigram/bigram
# The quickest way to get a sentence bagged as a trigram/bigram
bigram_mod = gensim.models.phrases.Phraser(bigram_model)

# Building the trigram model
trigram_mod = gensim.models.phrases.Phraser(trigram_model)


def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]


def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]


model_dataframe['3gram_reviews'] = make_trigrams(model_dataframe['clean_reviews'])

model_dataframe['3grams_nouns'] = model_dataframe['3gram_reviews'].map(lambda x: spacy_lemma(x))

model_dataframe['3grams_nouns_verbs'] = model_dataframe['3gram_reviews'].map(
    
    lambda x: spacy_lemma(x, allowed_postags=['NOUN', 'VERB']))

#saving the trained model to the file after execution of the code
#this is done in order to get the good trained models
model_dataframe.to_csv("./dataframes/final_df.csv")
