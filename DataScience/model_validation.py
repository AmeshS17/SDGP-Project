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

dominant_topic_dataframe = topic_sent.reset_index()
# set the columns of the data set
dominant_topic_dataframe.columns = ['document_no', 'dominant_topic', 'topic_perc_contrib', 'keywords', 'tokens',
                                    'original_text']
# count the total number of tokens and assign  to a column
dominant_topic_dataframe['num_tokens'] = dominant_topic_dataframe['tokens'].map(lambda x: len(x))
# add unique tokens to a column
dominant_topic_dataframe['unique_tokens'] = dominant_topic_dataframe['tokens'].map(lambda x: list(set(x)))
# count the number unique tokens and add to a column
dominant_topic_dataframe['num_unique_tokens'] = dominant_topic_dataframe['unique_tokens'].map(lambda x: len(x))
dominant_topic_dataframe = dominant_topic_dataframe[
    ['dominant_topic', 'original_text', 'topic_perc_contrib', 'tokens', 'num_tokens', 'unique_tokens',
     'num_unique_tokens', 'keywords']]
dominant_topic_dataframe.head(10)

# calculate the average (using median here) number of tokens to cut off overly lengthy reviews
check_tokens = dominant_topic_dataframe['num_tokens'].median()
# keep only the reviews with tokens less than or equal to the median
tokens_df = dominant_topic_dataframe[dominant_topic_dataframe['num_tokens'] <= check_tokens]
tokens_df.head()

# check the proportion of reviews assigned to each topic
cls_balance = tokens_df['dominant_topic'].value_counts(normalize=True)
print(cls_balance)
cls_balance.plot(kind='barh')

# Sample 5% of the dataset randomly and write to csv
sample_dataframe = tokens_df.sample(frac=0.05, random_state=1337)
sample_dataframe.to_csv('./dataframes/sample_dataframe.csv')


# manually label the csv file exported above marking 1 when dominant topic is correctly identified and 0 for
# misclassification
sample_dataframe_mod = pd.read_csv('./dataframes/sample_tokens_df_mod.csv', index_col=0)

samp_dataframe = sample_dataframe_mod.groupby(['num_tokens', 'correct'], as_index=False).count()[
    ['num_tokens', 'correct', 'dominant_topic']]

# set columns
samp_dataframe.columns = ['num_tokens', 'correct', 'count']
# view the correct & total counts as number of tokens changes
samp_dataframe

# use number of tokens less than or equal to 80th percentile
trunc_samp_2_df = samp_dataframe[samp_dataframe['num_tokens'] <= (np.percentile(sample_dataframe_mod['num_tokens'], 80))]
# turn unique number of tokens (no repeating values) into a list 
trunc_unique_num_tokens = list(trunc_samp_2_df['num_tokens'].unique())
       
