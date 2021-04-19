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

def identifyReviewTopics(ldamodel=lda_model, corpus=corpus, documents=documents):
    reviewTopicsDataframe = pd.DataFrame()
    #Taking the main topics in each documents
    for i, row in enumerate(ldamodel[corpus]):
        row = sorted(row, key=lambda x: (x[1]), reverse=True)
        #Taking the dominant topic, perc contribution and keywords for each documnet
        for j, (topicNumber, prop_topic) in enumerate(row):
            # Getting dominant topic
            if j == 0:  
                wp = ldamodel.show_topic(topicNumber)
                topicKeywords = ", ".join([word for word, prop in wp])
                # replaced int(topicNumber) with str(topicNumber)
                reviewTopicsDataframe = reviewTopicsDataframe.append(
                    pd.Series([topicDictionary[str(topicNumber)], round(prop_topic, 4), topicKeywords]),
                    ignore_index=True)  
            else:
                break
    reviewTopicsDataframe.columns = ['Dominant-Topoic', 'Contribution-Percentage', 'Keywords']
    # Adding the original text to the ouput of the document
    originalDataframe = pd.DataFrame(cleaned_data[['review', '3gram_reviews']])
    # docs = pd.Series(documents)
    reviewTopicsDataframe = pd.concat([reviewTopicsDataframe, originalDataframe], axis=1)
    return (reviewTopicsDataframe)

reviewTopicsDf = identifyReviewTopics()
sentAnalyzer = SentimentIntensityAnalyzer()
reviewTopicsDf['compound_sentiment'] = reviewTopicsDf['review'].map(lambda x: sentAnalyzer.polarity_scores(x)['compound'])
reviewTopicsDf.to_csv('C:/Users/Downloads/32323.csv')
sentimentDictionary = {}

# iterate through the topic dictionary
for topic in list(topicDictionary.values()):
    isCurrentTopic = reviewTopicsDf['Dominant_Topic'] == topic
    # filter out only the reviews where dominant topic is equal to current iteration
    topicDf = reviewTopicsDf[isCurrentTopic]
    sentimentList = topicDf['compound_sentiment']
    # populate pos,neg and neutral lists based on compound sentiment value
    positiveList = [x for x in sentimentList if x > 0.1]
    negativeList = [x for x in sentimentList if x < -0.1]
    neutralList = [x for x in sentimentList if x not in positiveList and x not in negativeList]
    totalList = len(sentimentList)
    # set if condition to avoid zero division error
    if totalList > 0:
        # calculate sentiment percentages
        positivePercentage = len(positiveList) / totalList
        neutralPercentage = len(neutralList) / totalList
        negativePercentage = len(negativeList) / totalList
        sentimentDictionary[topic] = [round(positivePercentage, 3), round(neutralPercentage, 3),
                                      round(negativePercentage, 3)]
        # output percentages as positive, neutral, then negative
sentimentDictionary
print("\nBy review\n", sentimentDictionary)
