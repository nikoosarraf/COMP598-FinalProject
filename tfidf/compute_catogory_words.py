import pandas as pd
import json
import os
import math
import argparse 

# this is the tfidf taught in class 
def tfidf(word, category):
    total_num = 0
    for word_count in altogether_counts.values():
        total_num += word_count

    freq = altogether_counts[word]

    freq_category = 0
    if word in annotated_counts[str(category)].keys():
        freq_category = annotated_counts[str(category)][word]

    return freq_category * math.log(total_num / freq)

# this is the way Derek asked us to do in his email 
def new_tfidf(word, category):
    topics_num  = 8
    categories = (1,2,3,4,5,6,7,8)
    
    topics_num_with_word = 0
    for i in categories:
        if word in wordcounts[str(i)].keys():
            topics_num_with_word += 1
    
    freq_category = wordcounts[str(category)][word]

    return freq_category * math.log(topics_num / topics_num_with_word)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('word_counts') 
    parser.add_argument('-o')
    args = parser.parse_args()
    
    global wordcounts 
    
    with open(args.word_counts, 'r') as fh:
        wordcounts = json.load(fh)
    
    
    tfidfs = {}
    results = {}
    categories = (1,2,3,4,5,6,7,8)
    for i in categories:
        for w in wordcounts[str(i)].keys():
            tfidfs[w] = new_tfidf(w, i)
        results[i] = sorted(tfidfs, key=tfidfs.get, reverse=True)[:10] 

    with open(args.o, "w") as fh:
        for j in categories:
            sub_results = {}
            sub_results[j] = results[j]
            json.dump(sub_results, fh, default=str)
            fh.write('\n')


if __name__=='__main__':
    main()
