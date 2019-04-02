import pandas as pd
import subprocess
import re
import os
import math


dem_df = pd.read_csv('~/POCA/data/dem_candidates.csv')
rep_df = pd.read_csv('~/POCA/data/rep_candidates.csv')
col_names = ['candidate', 'twitter_handle', 'date', 'original_text', 'stripped_text', 'retweets', 'favorites', 'geo', 'mentions', 'hashtags', 'media']

def remove_non_ascii(s): return "".join(i for i in s if ord(i)<128)

def remove_weird_characters(s):
    return re.sub('[^A-Za-z0-9\:\.\/\@\#\!\?\-\_\*]\w+', '', s)

def get_media_link(word):
    if 'pic.twitter' in word:
        pic_idx = word.index('pic.twitter')
        return word[pic_idx:], remove_non_ascii(word[:pic_idx])

    if 'http' in word:
        http_idx = word.index('http')
        return word[http_idx:], remove_non_ascii(word[:http_idx])

    return None, remove_non_ascii(word)

def strip_tweet(tweet):
    if type(tweet) != str:
        return tweet, [], [], []
    stripped = []
    s = tweet.split()
    hashtags = []
    mentions = []
    media = set()

    hashtag_check = False
    mention_check = False
    for i in range(len(s)):
        if s[i] == "@" and i < len(s) - 1:
            link, stripped_word = get_media_link(s[i + 1])
            if link:
                media.add(link)

            mentions.append("@" + stripped_word)
            mention_check = True

        elif s[i] == "#" and i < len(s) - 1:
            link, stripped_word = get_media_link(s[i + 1])
            if link:
                media.add(link)

            hashtags.append("#" + stripped_word)
            hashtag_check = True
        else:
            link, stripped_word = get_media_link(s[i])
            if link:
                media.add(link)

            if mention_check:
                mention_check = False
                stripped.append("@" + stripped_word)
            elif hashtag_check:
                hashtag_check = False
                stripped.append("#" + stripped_word)
            else:
                stripped.append(stripped_word)
            
    return " ".join(stripped), hashtags, mentions, media

already_got_tweets = pd.read_csv('../data/rep_already_got_tweets.csv').twitter_handle.unique()
already_got_tweets_candidates = pd.read_csv('../data/rep_already_got_tweets.csv').candidate.unique()
def write_tweets_to_data(twitter_handle, r):
    all_tweets = []
    tweet_text = False
    try: 
        if type(twitter_handle) == str:
            start_date = "2017-11-06"
            end_date = "2018-11-06"
            print("------- Getting tweets from {} to {} by {} -------".format(start_date, end_date, twitter_handle))
            bashCommand = "python3 /Users/katieta/GetOldTweets-python/Exporter.py --username {} --since {} --until {}".format(twitter_handle, start_date, end_date)
            out = subprocess.call(bashCommand.split())

            print("output: ", out)

            output_tweets = pd.read_csv('./output_got.csv', sep = ';', header = 'infer', encoding="ISO-8859-1", quotechar='"', error_bad_lines=False)
            # print(output_tweets)

            for i2, r2 in output_tweets.iterrows():
                tweet_text = r2['text']
                if type(tweet_text) == str:
                    stripped, hashtags, mentions, media = strip_tweet(tweet_text)
                    all_tweets.append([r['candidate'], twitter_handle, r2['date'], r2['text'], stripped, r2['retweets'], r2['favorites'], r2['geo'], mentions, hashtags, list(media)])

        with open('../data/rep_already_got_tweets.csv', 'a') as f:
            f.write('{}, {}\n'.format(twitter_handle, r['candidate']))

        df = pd.DataFrame(all_tweets, columns=col_names)

        # if file does not exist write header 
        if not os.path.isfile('../data/rep_tweets.csv'):
           df.to_csv('../data/rep_tweets.csv', header=True)
        else: # else it exists so append without writing the header
           df.to_csv('../data/rep_tweets.csv', mode='a', header=False)

    except Exception as e:
        if tweet_text:
            print(tweet_text, type(tweet_text))
        print("exception!")
        print(e)

def get_tweets_from_df(df):

    num_candidates = len(df)
    for i, r in df.iterrows():
        twitter_handle = r['twitter_handle']
        twitter_handle2 = r['twitter_handle2']

        if (twitter_handle in already_got_tweets and twitter_handle2 in already_got_tweets and type(twitter_handle2) == str) or (twitter_handle in already_got_tweets and type(twitter_handle2) != str):
            continue

        if (type(twitter_handle) != str and r['candidate'] in already_got_tweets_candidates):
            continue


        write_tweets_to_data(twitter_handle, r)
        if type(r['twitter_handle2']) == str:
            write_tweets_to_data(twitter_handle2, r)

        if i % 10 == 0:
            print("============================== finished {} / {} ==============================".format(i, num_candidates))

if __name__ == "__main__":
    get_tweets_from_df(rep_df)









