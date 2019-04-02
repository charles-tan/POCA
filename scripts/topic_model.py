import pandas as pd
import pickle
import random
from string import punctuation

import gensim
from gensim import corpora

import spacy
from spacy.lang.en import English


import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

# nltk.download('stopwords')
# nltk.download('wordnet')

dem_tweets = pd.read_csv('../data/tweet_data/dem_tweets_cleaned.csv')
rep_tweets = pd.read_csv('../data/tweet_data/rep_tweets_cleaned.csv')
dem_sampled_tweets = pd.read_csv('../data/tweet_data/dem_sampled_tweets.csv')
rep_sampled_tweets = pd.read_csv('../data/tweet_data/rep_sampled_tweets.csv')


rep_corpus = rep_tweets['stripped_text'].values
dem_corpus = dem_tweets['stripped_text'].values


parser = English()
def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
#         elif token.orth_.startswith('#'):
#             lda_tokens.append('HASHTAG')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens


def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens

def get_text_data(corpus):
    text_data = []
    for i in range(len(corpus)):
        if i % 20000 == 0:
            print("{} / {}".format(i, len(corpus)))
        try:
            tokens = prepare_text_for_lda(corpus[i])
            # if random.random() > .90 and full_data == False:
            #     text_data.append(tokens)
            # if full_data:
            text_data.append(tokens)
        except Exception as e:
            print(e)
    print("finished")
    return text_data

# remove common words and tokenize
list1 = ['RT','rt']
stoplist = stopwords.words('english') + list(punctuation) + list1
# print(stoplist)
en_stop = set(nltk.corpus.stopwords.words('english'))


def get_dict_corpus(text_data):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    return dictionary, corpus

def run_topic_model(text_data, num_topics, num_passes, num_words, model_name, save=True):
    dictionary = corpora.Dictionary(text_data)
    corpus = [dictionary.doc2bow(text) for text in text_data]
    
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = num_topics, id2word=dictionary, passes=num_passes)
    if save:
        ldamodel.save('topic_models/' + model_name + '.gensim')
    topics = ldamodel.print_topics(num_words=num_words)
    return topics

def print_topics(topics):
    for topic in topics:
        print(topic)

def main():

    # print("===================== democratic - full data =====================")
    # # dem_text_data = get_text_data(dem_corpus)
    # # pickle.dump(dem_text_data, open('dem_text_data.pkl', 'wb'))

    # with open('pickles/dem_text_data.pkl', 'rb') as f:
    #     dem_text_data = pickle.load(f)
    # topics = run_topic_model(text_data=dem_text_data
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='dem_model_15')
    # print_topics(topics)

    # print("===================== democratic - tweets longer than 4 words =====================")
    # # dem_long_tweets = dem_tweets[dem_tweets['stripped_text'].apply(lambda x: len(x.split(' ')) > 4)]
    # # dem_text_data_long = get_text_data(dem_long_tweets['stripped_text'].values)
    # # pickle.dump(dem_text_data_long, open('pickles/dem_text_data_long.pkl', 'wb'))

    # with open('pickles/dem_text_data_long.pkl', 'rb') as f:
    #     dem_text_data_long = pickle.load(f)

    # topics = run_topic_model(text_data=dem_text_data_long
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='dem_model_long_15')
    # print_topics(topics)

    # print("===================== democratic - sampled data =====================")
    # dem_sampled_text_data = get_text_data(dem_sampled_tweets['stripped_text'].values)
    # pickle.dump(dem_text_data_long, open('pickles/dem_sampled_text_data.pkl', 'wb'))

    # # with open('pickles/dem_sampled_text_data.pkl', 'rb') as f:
    # #     dem_sampled_text_data = pickle.load(f)

    # topics = run_topic_model(text_data=dem_sampled_text_data
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='dem_sampled_15'
    #                         , save=False)
    # print_topics(topics)



    # print("===================== republican - full data =====================")
    # # rep_text_data = get_text_data(rep_tweets['stripped_text'].values)
    # # pickle.dump(rep_text_data, open('pickles/rep_text_data.pkl', 'wb'))

    # with open('pickles/rep_text_data.pkl', 'rb') as f:
    #     rep_text_data = pickle.load(f)

    # topics = run_topic_model(text_data=rep_text_data
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='rep_model_15')
    # print_topics(topics)

    # print("===================== republican - tweets longer than 4 words =====================")
    # # rep_long_tweets = rep_tweets[rep_tweets['stripped_text'].apply(lambda x: len(x.split(' ')) > 4)]
    # # rep_text_data_long = get_text_data(rep_long_tweets['stripped_text'].values)
    # # pickle.dump(rep_text_data_long, open('pickles/rep_text_data_long.pkl', 'wb'))

    # with open('pickles/rep_text_data_long.pkl', 'rb') as f:
    #     rep_text_data_long = pickle.load(f)

    # # BEST RESULTS
    # topics = run_topic_model(text_data=rep_text_data_long
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='rep_model_long_15')
    # print_topics(topics)

    # print("===================== republican - sampled data =====================")
    # # rep_sampled_text_data = get_text_data(rep_sampled_tweets['stripped_text'].values)
    # # pickle.dump(rep_sampled_text_data, open('pickles/rep_sampled_text_data.pkl', 'wb'))

    # with open('pickles/rep_sampled_text_data.pkl', 'rb') as f:
    #     rep_sampled_text_data = pickle.load(f)

    # topics = run_topic_model(text_data=rep_sampled_text_data
    #                          , num_topics=15
    #                          , num_passes=15
    #                          , num_words=4
    #                          , model_name='rep_sampled_15')
    # print_topics(topics)

    print("===================== repub + dem - tweets longer than 4 words =====================")
    # rep_long_tweets = rep_tweets[rep_tweets['stripped_text'].apply(lambda x: len(x.split(' ')) > 4)]
    # rep_text_data_long = get_text_data(rep_long_tweets['stripped_text'].values)
    # pickle.dump(rep_text_data_long, open('pickles/rep_text_data_long.pkl', 'wb'))

    with open('pickles/rep_text_data_long.pkl', 'rb') as f:
        rep_text_data_long = pickle.load(f)

    with open('pickles/dem_text_data_long.pkl', 'rb') as f:
        dem_text_data_long = pickle.load(f)

    combined_text_data = rep_text_data_long + dem_text_data_long
    # BEST RESULTS
    topics = run_topic_model(text_data=combined_text_data
                             , num_topics=15
                             , num_passes=15
                             , num_words=4
                             , model_name='rep_model_long_15')
    print_topics(topics)

if __name__ == '__main__':
    main()
    
