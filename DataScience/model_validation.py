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

    # Map each topic number to a topic name using the topic list from previous step
topic_dict = {'0': 'Network Performance',
              '1': 'Overall Experience',
              '2': 'Gameplay Mechanics',
              '3': 'Content/Value',
              '4': 'NO TOPIC',
              }

# Identify the dominant topic for each review
def assign_topics(ldamodel=lda_model, corpus=corpus, documents=documents):
    sent_topics_df = pd.DataFrame()
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        for j, (topic_num, prop_topic) in enumerate(row):
            if j == 0:  # => dominant topic
                # Get the representation for a topic (list of word - probability pairs)
                wp = ldamodel.show_topic(topic_num)
                topic_keywords = ", ".join([word for word, prop in wp])
                # add dominant topic, percentage contribution and keywords to the topic dataframe
                sent_topics_df = sent_topics_df.append(
                    pd.Series([topic_dict[str(topic_num)], round(prop_topic, 4), topic_keywords]),
                    ignore_index=True)

            else:
                break
    # name the columns of the data frame
    sent_topics_df.columns = ['Dominant_Topic', 'Perc_Contribution', 'Topic_Keywords']

    # reference the original review 
    orig_contents = pd.Series(model_data_frame['review'])
    docs = pd.Series(documents)
    # add the original review column referenced above to the newly made dataframe
    sent_topics_df = pd.concat([sent_topics_df, docs, orig_contents], axis=1)
    return sent_topics_df


# use the function above to make a new data frame
topic_sent = assign_topics(ldamodel=lda_model, corpus=corpus, documents=documents)
# discard the rows that have "NO TOPIC" as the dominant topic
topic_sent = topic_sent[topic_sent['Dominant_Topic'] != 'NO TOPIC']
       
