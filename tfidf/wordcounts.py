import pandas as pd 
import argparse 
import json
import os.path as osp

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o')
    parser.add_argument('altogether_file')
    parser.add_argument('annotated_file')

    args = parser.parse_args()
    altogether = pd.read_csv(args.altogether_file, sep = '\t')
    annotated = pd.read_csv(args.annotated_file, sep = '\t')
    words_file = osp.join(osp.dirname(__file__),'words_alpha.txt')
    words_list = pd.read_csv(words_file, header=None)
    words_set = set(words_list[0].values.tolist())


# fill the coding column of the altogether df w/ 8s
# if the row exists in altogether_annoted, then replace the 8 w/ what we annotated 
    df =altogether.assign(coding = ['8']*2000)
    for name in annotated['name']:
        df.loc[df.name == name, 'coding'] = list(annotated.loc[annotated.name ==name, 'coding'])[0]


    punc_list = ["（", ")", "[", "]", ",", "-", ".", "?", "!", ":", ";", "#", "&"]
    categories = (1,2,3,4,5,6,7,8)
    results = {}

    for c in categories:
        catdf = df[df['coding'] == c]
        wordfreq = {}
        words = []
        for speech in catdf['title']:
            #replace punctuation marks w/ ' '
            speech = speech.translate({ord(a): " " for a in punc_list}).lower()
            for i in speech.split():
                 # remove non-words and words containing non-alpha characters
                if i.isalpha() and i in words_set:
                    words.append(i)
        freq = 0
        uniquewords = set(words)
        for w in uniquewords:
            freq = words.count(w)
            wordfreq[w] = freq

        results[c] = wordfreq
    
    with open(args.o, 'w') as fh:
        json.dump(results,fh)


if __name__ == '__main__':
    main()


