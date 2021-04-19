from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaMulticore
import string

# loading the dataframe
cleaned_data = pd.read_csv('./dataframes/final_df.csv', index_col=0, nrows=1000)

# selecting the 3grams_reviews for topic modeling
cleaned_data['3gram_reviews'] = cleaned_data['3gram_reviews'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())

# selecting the model
lda_model = LdaMulticore.load('.model/model.model')
documents = list(cleaned_data['3gram_reviews'])
dictionary = gensim.corpora.Dictionary(documents)

# loading the word dict
dictionary_saved = gensim.corpora.Dictionary.load('./model/model.model.id2word')
corpus = [dictionary_saved.doc2bow(text) for text in documents]

# making the topic dict
topicDictionary = {'0': 'Network Performance',
                   '1': 'Overall Experience',
                   '2': 'Gameplay Mechanics',
                   '3': 'Content/Value', 
                   '4': 'NO TOPIC',
                   }


