import json
import urllib.parse
import boto3
import csv
import io

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

s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

def get_csv(bucket,key):
    
    csv_object = s3.get_object(Bucket=bucket, Key=key)
    csv_content = csv_object['Body'].read().decode('utf-8').split('\n')
    
    csv_dict = list(csv.DictReader(csv_content))
    
    for row in csv_dict:
        author_playtime_forever = int(row['author.playtime_forever'])
        steam_purchase = row['steam_purchase'].lower() == 'true'
        received_for_free = row['received_for_free'].lower() == 'true'
        written_during_early_access = row['written_during_early_access'].lower() == 'true'
        update_dict = {"author.playtime_forever":author_playtime_forever,
                        "steam_purchase":steam_purchase,
                        "received_for_free":received_for_free,
                        "written_during_early_access":written_during_early_access}
        row.update(update_dict)


    print(csv_dict[:15])
    print("Data dictionary length : " + str(len(csv_dict)))
    
    return csv_dict


def put_csv(filebuffer,bucket,key):
    
    csv_object = filebuffer.getvalue()

    response = s3.put_object(Body=csv_object,Bucket=bucket,Key=key)

    print(response)
    return True


def invoke_model(key):
    response = lambda_client.invoke(
        FunctionName = 'generate_summary',
        InvocationType = 'Event',
        Payload = json.dumps({'filekey':key})
    )


def preprocess_data(review_data):

    parser = bbcode.Parser()


    cList = {
    "ain't": "am not",
    "aren't": "are not",
    "can't": "cannot",
    "can't've": "cannot have",
    "'cause": "because",
    "could've": "could have",
    "couldn't": "could not",
    "couldn't've": "could not have",
    "didn't": "did not",
    "doesn't": "does not",
    "don't": "do not",
    "hadn't": "had not",
    "hadn't've": "had not have",
    "hasn't": "has not",
    "haven't": "have not",
    "he'd": "he would",
    "he'd've": "he would have",
    "he'll": "he will",
    "he'll've": "he will have",
    "he's": "he is",
    "how'd": "how did",
    "how'd'y": "how do you",
    "how'll": "how will",
    "how's": "how is",
    "I'd": "I would",
    "I'd've": "I would have",
    "I'll": "I will",
    "I'll've": "I will have",
    "I'm": "I am",
    "I've": "I have",
    "isn't": "is not",
    "it'd": "it had",
    "it'd've": "it would have",
    "it'll": "it will",
    "it'll've": "it will have",
    "it's": "it is",
    "let's": "let us",
    "ma'am": "madam",
    "mayn't": "may not",
    "might've": "might have",
    "mightn't": "might not",
    "mightn't've": "might not have",
    "must've": "must have",
    "mustn't": "must not",
    "mustn't've": "must not have",
    "needn't": "need not",
    "needn't've": "need not have",
    "o'clock": "of the clock",
    "oughtn't": "ought not",
    "oughtn't've": "ought not have",
    "shan't": "shall not",
    "sha'n't": "shall not",
    "shan't've": "shall not have",
    "she'd": "she would",
    "she'd've": "she would have",
    "she'll": "she will",
    "she'll've": "she will have",
    "she's": "she is",
    "should've": "should have",
    "shouldn't": "should not",
    "shouldn't've": "should not have",
    "so've": "so have",
    "so's": "so is",
    "that'd": "that would",
    "that'd've": "that would have",
    "that's": "that is",
    "there'd": "there had",
    "there'd've": "there would have",
    "there's": "there is",
    "they'd": "they would",
    "they'd've": "they would have",
    "they'll": "they will",
    "they'll've": "they will have",
    "they're": "they are",
    "they've": "they have",
    "to've": "to have",
    "wasn't": "was not",
    "we'd": "we had",
    "we'd've": "we would have",
    "we'll": "we will",
    "we'll've": "we will have",
    "we're": "we are",
    "we've": "we have",
    "weren't": "were not",
    "what'll": "what will",
    "what'll've": "what will have",
    "what're": "what are",
    "what's": "what is",
    "what've": "what have",
    "when's": "when is",
    "when've": "when have",
    "where'd": "where did",
    "where's": "where is",
    "where've": "where have",
    "who'll": "who will",
    "who'll've": "who will have",
    "who's": "who is",
    "who've": "who have",
    "why's": "why is",
    "why've": "why have",
    "will've": "will have",
    "won't": "will not",
    "won't've": "will not have",
    "would've": "would have",
    "wouldn't": "would not",
    "wouldn't've": "would not have",
    "y'all": "you all",
    "y'alls": "you alls",
    "y'all'd": "you all would",
    "y'all'd've": "you all would have",
    "y'all're": "you all are",
    "y'all've": "you all have",
    "you'd": "you had",
    "you'd've": "you would have",
    "you'll": "you you will",
    "you'll've": "you you will have",
    "you're": "you are",
    "you've": "you have"
    }

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


    #INPUT DATA
    review_data = review_data

    # making pandas readable format from input data
    steam_reviews_dict = {'recommendationid': [review_data[i]['recommendationid'] for i in range(len(review_data))],

                        'author.steamid': [review_data[i]['author.steamid'] for i in range(len(review_data))],

                        'author.num_games_owned': [review_data[i]['author.num_games_owned'] for i in
                                                    range(len(review_data))],

                        'author.num_reviews': [review_data[i]['author.num_reviews'] for i in range(len(review_data))],

                        'author.playtime_forever': [review_data[i]['author.playtime_forever'] for i in
                                                    range(len(review_data))],

                        'author.playtime_last_two_weeks': [review_data[i]['author.playtime_last_two_weeks'] for i in
                                                            range(len(review_data))],

                        'author.last_played': [review_data[i]['author.last_played'] for i in range(len(review_data))],

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

    data_frame_raw['author.playtime_forever'] = data_frame_raw['author.playtime_forever'] / 60

    data_frame_raw['author.playtime_last_two_weeks'] = data_frame_raw['author.playtime_last_two_weeks'] / 60

    data_frame_raw['review_length'] = data_frame_raw['review'].map(lambda x: len(x.split()))

    data_frame_raw_num = data_frame_raw.select_dtypes(exclude=['O', 'bool'])

    dataframe_usable = data_frame_raw[
        (data_frame_raw['author.playtime_forever'] >= 8)]

    dataframe_usable['review_length'] = dataframe_usable['review'].map(lambda x: len(x.split()))

    #setting percentile to 40% to get rid of overly short reviews

    dataframe_ready = dataframe_usable[
        dataframe_usable['review_length'] > np.percentile(dataframe_usable['review_length'], 40)].reset_index(drop=True)

    dataframe_cleaning = dataframe_ready.drop_duplicates(subset=['author.steamid', 'review'])

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
    bigram = gensim.models.Phrases(list(model_dataframe['clean_reviews']), min_count=5,
                                threshold=10)  # feed a list of lists of words e.g. [['word1','word2'],['word3',
    # 'word4'] to get bigrams]
    trigram = gensim.models.Phrases(bigram[list(model_dataframe['clean_reviews'])], threshold=10)

    # Faster way to get a sentence clubbed as a trigram/bigram
    bigram_mod = gensim.models.phrases.Phraser(bigram)
    trigram_mod = gensim.models.phrases.Phraser(trigram)

    def make_bigrams(texts):
        return [bigram_mod[doc] for doc in texts]


    def make_trigrams(texts):
        return [trigram_mod[bigram_mod[doc]] for doc in texts]


    model_dataframe['3gram_reviews'] = make_trigrams(model_dataframe['clean_reviews'])
    model_dataframe['3grams_nouns'] = model_dataframe['3gram_reviews'].map(lambda x: spacy_lemma(x))
    model_dataframe['3grams_nouns_verbs'] = model_dataframe['3gram_reviews'].map(
        lambda x: spacy_lemma(x, allowed_postags=['NOUN', 'VERB']))

    filebuffer = io.StringIO()

    model_dataframe.to_csv(filebuffer)

    #OUTPUT AS STRINGIO BUFFER
    return filebuffer


def lambda_handler(event, context):

    print("Invocation event - " + str(event))

    # Get the object from the event and show its content type
    get_bucket = event['Records'][0]['s3']['bucket']['name']
    put_bucket = 'cleaned-csv-files'
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    
    waiter = s3.get_waiter('object_exists')
    waiter.wait(
        Bucket=get_bucket,
        Key=key,
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts':12
        }
    )
    
    try:
        data_dict = get_csv(get_bucket,key)
    
        cleaned_result_buffer = preprocess_data(data_dict)
        uploaded = put_csv(cleaned_result_buffer,put_bucket,key)
        
        waiter.wait(
        Bucket=put_bucket,
        Key=key,
        WaiterConfig={
            'Delay': 5,
            'MaxAttempts':12
            }
        )
    
        invoke_model(key)
        return None
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, get_bucket))
        raise e


