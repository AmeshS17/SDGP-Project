import string
import gensim
from gensim.models import LdaMulticore
from gensim import corpora
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# read the cleaned data frame
model_data_frame = pd.read_csv('./dataframes/model2_df.csv', index_col=0)

# load the trained model
lda_model = LdaMulticore.load('./models/nouns_only/model/model.model')

# Turn the required columns of data into lists to be used in creating a dictionary (using doc2bow) in the next few steps 
model_data_frame['clean_reviews'] = model_data_frame['clean_reviews'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())
model_data_frame['3grams_nouns'] = model_data_frame['3grams_nouns'].map(
    lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())

documents = list(model_data_frame['3grams_nouns'])
dictionary = gensim.corpora.Dictionary(documents)
# reload the dictionary that was created during model creation
dictionary_saved = gensim.corpora.Dictionary.load(
    './models/nouns_only/model/model.model.id2word')  # this dictionary already had filter_extremes() applied during
# training step
corpus = [dictionary_saved.doc2bow(text) for text in documents]
# print the keywords associated with each topic
topic_list = lda_model.print_topics(num_topics=5, num_words=15)
for index, i in enumerate(topic_list):
    str1 = str(i[1])
    for c in "0123456789+*\".":
        str1 = str1.replace(c, "")
    str1 = str1.replace("  ", " ")
    print(str1)

