import json
import urllib.parse
import boto3
import csv
import io

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import gensim
from gensim import corpora
from gensim.models import LdaMulticore
import string

s3 = boto3.client('s3')

def get_csv(bucket,key):
    
    csv_object = s3.get_object(Bucket=bucket, Key=key)
    csv_content = io.StringIO(csv_object['Body'].read().decode('utf-8'))
    
    return csv_content


def put_json(csv_dict,bucket,key):
    #sample_dict = csv_dict[:5]
    
    response = s3.put_object(Body=json.dumps(csv_dict).encode('utf-8'),Bucket=bucket,Key=key)

    print(response)
    return True


def summarize(csv_content):

    cleaned_data = pd.read_csv(csv_content, index_col=0, nrows=1000)
    cleaned_data['3gram_reviews'] = cleaned_data['3gram_reviews'].map(
        lambda x: ''.join(c for c in x if c == '_' or c not in string.punctuation).split())
    lda_model = LdaMulticore.load('model.model')
    documents = list(cleaned_data['3gram_reviews'])
    dictionary = gensim.corpora.Dictionary(documents)
    dictionary_saved = gensim.corpora.Dictionary.load('model.model.id2word')
    corpus = [dictionary_saved.doc2bow(text) for text in documents]

    topicDictionary = {'0': 'Network Performance',
                        '1': 'Overall Experience',
                        '2': 'Gameplay Mechanics',
                        '3': 'Content/Value', 
                        '4': 'NO TOPIC',
                    }


    def identifyReviewTopics(ldamodel=lda_model, corpus=corpus, documents=documents):
        reviewTopicsDataframe = pd.DataFrame()
        # Get main topic in each document
        for i, row in enumerate(ldamodel[corpus]):
            row = sorted(row, key=lambda x: (x[1]), reverse=True)
            # Get the Dominant topic, Perc Contribution and Keywords for each document
            for j, (topicNumber, prop_topic) in enumerate(row):
                if j == 0:  
                    wp = ldamodel.show_topic(topicNumber)
                    topicKeywords = ", ".join([word for word, prop in wp])
                    reviewTopicsDataframe = reviewTopicsDataframe.append(
                        pd.Series([topicDictionary[str(topicNumber)], round(prop_topic, 4), topicKeywords]),
                        ignore_index=True)  # replaced int(topicNumber) with str(topicNumber)
                else:
                    break
        reviewTopicsDataframe.columns = ['Dominant_Topic', 'Contribution_Percentage', 'Keywords']
        # Add original text to the end of the output
        originalDataframe = pd.DataFrame(cleaned_data[['review', '3gram_reviews']])
        reviewTopicsDataframe = pd.concat([reviewTopicsDataframe, originalDataframe], axis=1)
        return reviewTopicsDataframe


    reviewTopicsDf = identifyReviewTopics()
    sentAnalyzer = SentimentIntensityAnalyzer()
    reviewTopicsDf['compound_sentiment'] = reviewTopicsDf['review'].map(lambda x: sentAnalyzer.polarity_scores(x)['compound'])
    sentimentDictionary = {}

    for topic in list(topicDictionary.values()):
        isCurrentTopic = reviewTopicsDf['Dominant_Topic'] == topic
        topicDf = reviewTopicsDf[isCurrentTopic]
        sentimentList = topicDf['compound_sentiment']
        positiveList = [x for x in sentimentList if x > 0.1]
        negativeList = [x for x in sentimentList if x < -0.1]
        neutralList = [x for x in sentimentList if x not in positiveList and x not in negativeList]
        totalList = len(sentimentList)
        print(topic)
        print(totalList)
        if (totalList > 0):
            positivePercentage = len(positiveList) / totalList
            neutralPercentage = len(neutralList) / totalList
            negativePercentage = len(negativeList) / totalList
            sentimentDictionary[topic] = [round(positivePercentage, 3), round(neutralPercentage, 3), round(negativePercentage, 3)]
            # output percentages as positive, neutral, then negative
    print("\nBy review\n", sentimentDictionary)


    return sentiment_dictionary


def lambda_handler(event, context):

    print("Invocation event - " + str(event))

    # Get the object from the event and show its content type
    get_bucket = 'cleaned-csv-files'
    put_bucket = 'summary-json-files'
    get_key = event['filekey']
    
    waiter = s3.get_waiter('object_exists')
    waiter.wait(
        Bucket=get_bucket,
        Key=get_key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
        }
    )
    
    try:
        csv_content = get_csv(get_bucket,get_key)
        
        sentiment_dictionary = summarize(csv_content)
        
        put_key = get_key[:-3] + 'json'
        uploaded = put_json(sentiment_dictionary,put_bucket,put_key)
        
        waiter.wait(
        Bucket=put_bucket,
        Key=put_key,
        WaiterConfig={
            'Delay': 10,
            'MaxAttempts':15
        }
    )
        
        return None
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(get_key, get_bucket))
        raise e


