# count num of pos, neg, unkown tweets for each candidate and add it to their csv files

import csv

negative = {}
neutral = {}
positive = {}
with open('../data/sa_all_tweets_post.csv', 'r') as pred_results:
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


def write_to_csv(reader, output_csv):
    for i, line in enumerate(reader):
        out = ",".join(line)
        out += ","

        if i == 0:
            output_csv.write(out + "count_negative,count_neutral,count_positive,sentiment\n")
            continue

        twitter_handle = line[1]
        if twitter_handle == "":
            output_csv.write(out + ",,,\n")
            continue

        sentiment = 0.0
        total = 0.0

        if not twitter_handle in negative:
            out += "0,"
        else:
            out += str(negative[twitter_handle]) + ","
            total += negative[twitter_handle]

        if not twitter_handle in neutral:
            out += "0,"
        else:
            out += str(neutral[twitter_handle]) + ","
            sentiment += neutral[twitter_handle] * 2
            total += neutral[twitter_handle]

        if not twitter_handle in positive:
            out += "0,"
        else:
            out += str(positive[twitter_handle]) + ","
            sentiment += positive[twitter_handle] * 4
            total += positive[twitter_handle]

        if total > 0:
            out += str(sentiment / total)
        out += '\n'
        output_csv.write(out)



with open('../data/dem_candidates.csv', 'r') as dem_csv:
    reader = csv.reader(dem_csv)
    with open('../data/post_dem_candidates.csv', 'w') as post_dem_csv:
        write_to_csv(reader, post_dem_csv)
        
with open('../data/rep_candidates.csv', 'r', encoding="ISO-8859-1") as rep_csv:
    reader = csv.reader(rep_csv)
    with open('../data/post_rep_candidates.csv', 'w') as post_rep_csv:
        write_to_csv(reader, post_rep_csv)

