# count num of pos, neg, unkown tweets for each candidate and add it to their csv files

import csv

negative = {}
neutral = {}
positive = {}
with open('../data/tweet_data/sa_all_tweets_post.csv', 'r') as pred_results:
    reader = csv.reader(pred_results)
    for i, line in enumerate(reader):
        if i == 0:
            continue
        if int(line[3]) == 0:
            if not line[2] in negative:
                negative[line[2]] = 1 
            else:
                negative[line[2]] += 1
        elif int(line[3]) == 4:
            if not line[2] in positive:
                positive[line[2]] = 1 
            else:
                positive[line[2]] += 1
        else:
            if not line[2] in neutral:
                neutral[line[2]] = 1 
            else:
                neutral[line[2]] += 1

def twitter_handle_to_sentiment_tweets_count(twitter_handle):
    negative_count = 0
    neutral_count = 0
    positive_count = 0
    if twitter_handle in negative:
        negative_count = negative[twitter_handle]

    if twitter_handle in neutral:
        neutral_count = neutral[twitter_handle]

    if twitter_handle in positive:
        positive_count = positive[twitter_handle]
    return (negative_count, neutral_count, positive_count)

def write_to_csv(reader, output_csv):
    for i, line in enumerate(reader):
        out = ",".join(line)
        out += ","

        if i == 0:
            output_csv.write(out + "count_negative,count_neutral,count_positive,sentiment\n")
            continue

        twitter_handle = line[1]
        twitter_handle2 = line[2]

        # if twitter_handle == "":
        #     output_csv.write(out + "0,0,0,-1\n")
        #     continue


        sentiment = 0.0
        total = 0.0
        negative_count1, neutral_count1, positive_count1 = twitter_handle_to_sentiment_tweets_count(twitter_handle)
        negative_count2, neutral_count2, positive_count2 = twitter_handle_to_sentiment_tweets_count(twitter_handle2)
        negative_count, neutral_count, positive_count = negative_count1 + negative_count2, neutral_count2 + neutral_count1, positive_count2 + positive_count1
        total += negative_count + neutral_count + positive_count
        sentiment += neutral_count * 2 + positive_count * 4

        out += str(negative_count) + "," + str(neutral_count) + "," + str(positive_count) + ","

        if total > 0:
            out += str(sentiment / total)
        #else:  
        #    out += "NaN"
        out += '\n'
        output_csv.write(out)
        

with open('../data/dem_candidates_with_tweet_topics.csv', 'r') as dem_csv:
    reader = csv.reader(dem_csv)
    with open('../data/post_dem_candidates_with_tweet_topics.csv', 'w') as post_dem_csv:
        write_to_csv(reader, post_dem_csv)
        
with open('../data/rep_candidates_with_tweet_topics.csv', 'r', encoding="ISO-8859-1") as rep_csv:
    reader = csv.reader(rep_csv)
    with open('../data/post_rep_candidates_with_tweet_topics.csv', 'w') as post_rep_csv:
        write_to_csv(reader, post_rep_csv)

