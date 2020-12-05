import requests
import json
import os
from datetime import datetime
import time
import csv

# CONSTANTS
num_posts = 333
subs = ['politics']
categories = ['hot']
output_dir = 'raw_data'
current_time = datetime.now().strftime("%Y-%m-%d")

"""
Pull data from Reddit API, given:
    subreddit
    category (e.g. Top)
    output file
    filter function
    output file for filtered data
    after marker
Returns the next after
"""
def hit_api(sub_name, category, output_file, filter_func, filtered_output, after):
    data = requests.get(f'https://api.reddit.com/r/{sub_name}/{category}/?t=day&limit=100&after={after}', 
        headers={'User-Agent': 'macos: requests (by /u/school_reddit_acc)'})
    content = data.json()['data']
    posts = content['children'] # type list
    with open(output_file, 'a') as f: # append each post to the output file
        with open(filtered_output, 'a') as g:
            writer_f = csv.writer(f, delimiter='\t')
            writer_g = csv.writer(g, delimiter='\t')
            writer_f.writerow(['name', 'title'])
            for post in posts:
                data = post['data']
                writer_f.writerow([data['name'], data['title']])
                if(filter_func(data)):
                    writer_g.writerow([data['name'], data['title']])
    return content['after'] # for the next iteration

"""
Input: post in dictionary form
Output: True if post mentions Biden or Trump, case-insensitive, False otherwise
"""
def mentions(data):
    title = data['title']
    return True if 'trump' in title.lower() or 'biden' in title.lower() else False

def main():
    after = ""
    for i in range(4):
        # iteration i uses `after` returned in iteration i-1
        for sub_name in subs:
            for category in categories:
                filename = f'{current_time}_{sub_name}_{category}'
                output_file = os.path.join(os.getcwd(), output_dir, f'{filename}.tsv')
                filtered_output = os.path.join(os.getcwd(), output_dir, f'{filename}_filtered.tsv')
                print(after)
                after = hit_api(sub_name, category, output_file, mentions, filtered_output, after)

if __name__ == '__main__':
    main()