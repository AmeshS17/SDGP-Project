# reading the data from the dataset and converting to lowercase, converting list of reviews
import pandas as pd
import nltk
from string import punctuation as punc
from sklearn.feature_extraction._stop_words import ENGLISH_STOP_WORDS
from nltk.stem import WordNetLemmatizer

dataset = pd.read_csv('dark.csv')
reviews = dataset['review']

reviews_list = []

'''
1.	CC	Coordinating conjunction
2.	CD	Cardinal number
3.	DT	Determiner
4.	EX	Existential there
5.	FW	Foreign word
6.	IN	Preposition or subordinating conjunction
7.	JJ	Adjective
8.	JJR	Adjective, comparative
9.	JJS	Adjective, superlative
10.	LS	List item marker
11.	MD	Modal
12.	NN	Noun, singular or mass
13.	NNS	Noun, plural
14.	NNP	Proper noun, singular
15.	NNPS	Proper noun, plural
16.	PDT	Predeterminer
17.	POS	Possessive ending
18.	PRP	Personal pronoun
19.	PRP$	Possessive pronoun
20.	RB	Adverb
21.	RBR	Adverb, comparative
22.	RBS	Adverb, superlative
23.	RP	Particle
24.	SYM	Symbol
25.	TO	to
26.	UH	Interjection
27.	VB	Verb, base form
28.	VBD	Verb, past tense
29.	VBG	Verb, gerund or present participle
30.	VBN	Verb, past participle
31.	VBP	Verb, non-3rd person singular present
32.	VBZ	Verb, 3rd person singular present
33.	WDT	Wh-determiner
34.	WP	Wh-pronoun
35.	WP$	Possessive wh-pronoun
36.	WRB	Wh-adverb
'''

for review in reviews:
    review = nltk.sent_tokenize(str(review))
    for sen in review:
        sen = sen.lower()
        sen = nltk.word_tokenize(sen)
        reviews_list.append(sen)
        
pdoc = []
allowed_tags = ['VBP', 'VB', 'VBG', 'JJ', 'NN', 'RB']
bad_word = ['fuck', "shit"]

lemmatizer = WordNetLemmatizer()

for sen in reviews_list:
    sen = [lemmatizer.lemmatize(word) for word in sen]
    tagged = nltk.pos_tag(sen)
    for w, t in tagged:
        if w in punc:
            sen.remove(w)
        elif w in ENGLISH_STOP_WORDS:
            sen.remove(w)
        elif t not in allowed_tags:
            sen.remove(w)
    pd = ' '.join(sen)
    pdoc.append(pd)



    
