import pandas as pd
import subprocess
import re


dem_df = pd.read_csv('~/POCA/data/dem_candidates.csv')
col_names = ['candidate', 'twitter_handle', 'date', 'text', 'stripped_text', 'retweets', 'favorites', 'geo', 'mentions', 'hashtags', 'media']
all_tweets = []
i = 0

# result = subprocess.Popen(['/usr/bin/flock -n', 'blah.lockfile', 'python3 executer.py', 'some_arg' ,'&'])
# result = subprocess.Popen(['/usr/bin/flock', '-n', 'blah.lockfile', 'python3 executer.py', 'some_arg', '&'])
# def remove_link(word):

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


for i, r in dem_df.iterrows():
    if i == 2:
        break

    twitter_handle = r['twitter_handle']
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
            stripped, hashtags, mentions, media = strip_tweet(r2['text'])
            all_tweets.append([r['candidate'], twitter_handle, r2['date'], r2['text'], stripped, r2['retweets'], r2['favorites'], r2['geo'], mentions, hashtags, list(media)])


pd.DataFrame(all_tweets, columns=col_names).to_csv('~/POCA/data/all_tweets.csv', index=False)



