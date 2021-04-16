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

# build a dictionary & corpus based on the nouns column
document = list(modelDataframe['3grams_nouns'])
dictionary = gensim.corpora.Dictionary(document)
dictionary.filter_extremes(no_below=10, no_above=0.5)
corpus = [dictionary.doc2bow(word) for word in document]

# run the training in a loop since we can amass a large number of models and evaluate them later
for loopNum in range(2):
    # randomize the number of topics and passes within a reasonable range as the variation has a chance to produce an
    # effective model
    numberOfTopics = random.randint(5, 8)
    passes = random.randint(100, 120)
    eval_every = None
    seed = np.random.randint(0, 999999)
    print("Seed:", seed, "\n")

    ldaModel = LdaMulticore(corpus, num_topics=numberOfTopics, id2word=dictionary, passes=passes, alpha='asymmetric',
                            eval_every=eval_every, workers=3, random_state=seed)

    # Check resulting topics.
    listOfTopics = ldaModel.print_topics(num_topics=numberOfTopics, num_words=15)
    for index, i in enumerate(listOfTopics):
        string = str(i[1])
        for c in "0123456789+*\".":
            string = string.replace(c, "")
        string = string.replace("  ", " ")
        print(string) 
     # calculate & display perplexity
    print('\nPerplexity: ', ldaModel.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

    # calculate & display coherence
    coherenceModel = CoherenceModel(model=ldaModel, texts=document, dictionary=dictionary, coherence='c_v')
    ldaCoherence = coherenceModel.get_coherence()
    print('\nCoherence Score: ', ldaCoherence)
    
     # assign a file name based on the loop number so that models aren't overridden during successive iterations.
    path = './models/both/nouns_only'
    if not os.path.exists(path):
        os.makedirs(path)
    ldaModel.save(f'./models/both/nouns_only/model1-{loopNum}.model')        
