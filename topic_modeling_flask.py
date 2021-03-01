# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
import json

data = pd.read_csv('C:/Users/Luxman/Downloads/389730_TEKKEN7_.csv', error_bad_lines=False);
data_text = data[['review']]
data_text['index'] = data_text.index
documents = data_text
print(len(documents))
print(documents[:4311])

import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.stem.porter import *
import numpy as np

np.random.seed(2018)
import nltk

nltk.download('wordnet')

import pandas as pd

data = pd.read_csv('C:/Users/Luxman/Downloads/389730_TEKKEN7_.csv', error_bad_lines=False);
data_text = data[['review']]
data_text['index'] = data_text.index
documents = data_text


def lemmatize_stemming(text):
    return (WordNetLemmatizer().lemmatize(text, pos='v'))


def preprocess(text):
    result = []
    for token in gensim.utils.simple_preprocess(text):
        if token not in gensim.parsing.preprocessing.STOPWORDS and len(token) > 3:
            result.append(lemmatize_stemming(token))
    return result


doc_sample = documents[documents['index'] == 200].values[0][0]
print('original document: ')
words = []
for word in doc_sample.split(' '):
    words.append(word)
print(words)
print('\n\n tokenized and lemmatized document: ')
print(preprocess(doc_sample))

processed_docs = documents['review'].astype(str).map(preprocess)
processed_docs[:100]

dictionary = gensim.corpora.Dictionary(processed_docs)
myLis = []
count = 0
for k, v in dictionary.iteritems():
    myLis.append(v)
    print(k, v)
    count += 1
    if count > 10:
        break
dictionary.filter_extremes(no_below=15, no_above=0.5, keep_n=100000)

myJson = "{" + "\"Game\": [" + "{"
for i in range(1, 11):
    if i == 10:
        myJson += f"\"topic{i}\" :" + "\"" + myLis[i] + "\""
    else:
        myJson += f"\"topic{i}\" :" + "\"" + myLis[i] + "\"" + ","
myJson += "}" + "]" + "} "

bow_corpus = [dictionary.doc2bow(doc) for doc in processed_docs]
bow_corpus[4310]
bow_doc_4310 = bow_corpus[4310]
for i in range(len(bow_doc_4310)):
    print("Word {} (\"{}\") appears {} time.".format(bow_doc_4310[i][0], dictionary[bow_doc_4310[i][0]],
                                                     bow_doc_4310[i][1]))

from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route('/game')
def hello_admin():
    return myJson


if __name__ == '__main__':
    app.run(debug=True)
