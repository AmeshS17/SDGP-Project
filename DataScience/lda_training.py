import numpy as np
import pandas as pd
import random
import string
import gensim
from gensim import corpora
from gensim.models import CoherenceModel, LdaMulticore
from gensim.parsing.preprocessing import STOPWORDS
import os

# read the file that is produced from the review cleaning process (cleaned dataset)
modelDataframe = pd.read_csv('./dataframes/final_df.csv', index_col=0)

# remove punctuation for all columns of the clean dataset
modelDataframe['clean_reviews'] = modelDataframe['clean_reviews'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())
modelDataframe['3gram_reviews'] = modelDataframe['3gram_reviews'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())
modelDataframe['3grams_nouns'] = modelDataframe['3grams_nouns'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())
modelDataframe['3grams_nouns_verbs'] = modelDataframe['3grams_nouns_verbs'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())

# use this dictionary to convert numbers to text
number_dictionary = {'0': 'zero',
            '1': 'one',
            '2': 'two',
            '3': 'three',
            'ii': 'two',
            'iii': 'three'}

def num2words(d):
    if (len(d) == 1 and d in '0123') or (d in ['ii', 'iii']):
        word = number_dictionary[d]

    elif len(str(d)) == 1 and str(d) in '0123':
        word = number_dictionary(str(d))

    else:
        word = d
    return word


# added stopwords based on the output of the model. Meaningless words that generated noise were added progressively
# while training the model
stopwords = list(set(STOPWORDS))
stopwords.extend(
    ['good', 'better', 'great', 'lot', 'game', 'like', 'I', 'i', 'one', 'two', 'three', 'one_best_fighting_games',
     'fighting_games', 'fighting_games', 'thing', 'bit', 'street_fighter', 'time', '10_10', 'love', 'fun', 'play',
     'hour', 'sfv',
     'fighting', 'tekken', 'best_fighting', 'character', 'story_mode', 'fighter', 'fighting', 'street_fighter',
     'arcade_mode', 'try', 'come', 'better', 'learn', 'great',
     'best_fighting_game', 'lot', 'game', "tekken", "play", "fun", "love", "character", "fuck", "suck", "shit", 'thing',
     "capcom", 'krypt', "best_fighting",
     "fighting_games", "street_fighter", "tekken", "mortal_kombat", "mk", "mkx", "hate", "fighting_game",
     'street_fighter', 'towers_time', 'tower'])


# function that changes numbers to words by calling Number_2_words() and removes stopwords
def removeStopwords(doc):
    words = [num2words(w) for w in doc if w != '' and w not in stopwords]
    return words


modelDataframe['3grams_nouns'] = modelDataframe['3grams_nouns'].map(lambda x: removeStopwords(x))
modelDataframe['3grams_nouns_verbs'] = modelDataframe['3grams_nouns_verbs'].map(lambda x: removeStopwords(x))

