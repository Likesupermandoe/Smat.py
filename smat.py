#!/usr/bin/python3

#./smat.py -s [searchword(s)] -i [source] -o [filename.csv]
#https://api.smat-app.com/docs

import argparse
import requests
import json
import pandas as pd
import csv


def main():
        parser = argparse.ArgumentParser(description='Make a command line that searches smat and exports the searches into the CSV format')
        parser.add_argument('-t', '--term', required=True, help='keyword you want to search')
        parser.add_argument('-l', '--limit', type=int, default='10', required=True, help='number of posts to search from site')
        parser.add_argument('-s', '--site', required=True, help='reddit, 4chan, twitter')
        parser.add_argument('-o', '--output', help='output result as a csv file')
        args = parser.parse_args()
        with open(args.output, 'w') as output_file:
                output_file.write(str(api_data(args.term, args.limit, args.site)))

def data_framing(data):
        df = pd.DataFrame(data)
        hits_dict = data['hits']['hits']
        df2 = pd.DataFrame(hits_dict)
        df_source = df2['_source']
        info_list = []
        for dic in df_source:
                info_list.append(dic)
        return pd.DataFrame(info_list)

def api_data(term, limit, site):
        response = requests.get('https://api.smat-app.com/content?term=' + term + '&limit=' + str(limit) +'&site=' + site +'&since=2020-12-16T14%3A46%3A35.530872&until=2021-02-16T14%3A46%3A35.530872&esquery=false')
        data = json.loads(response.text)
        df = data_framing(data)

        website = {"reddit": ['body', 'subreddit', 'link_id', 'subreddit_id', 'created_utc', 'author_fullname', 'author', 'permalink', 'parent_id', 'retrieved_on', 'score'], 
        "4chan": ['com', 'now', 'name', 'country', 'countryname','board'], 
        "twitter": ['created_at', 'in_reply_to_user_id_str', 'source', 'user_id', 'in_reply_to_screen_name', 'entities', 'screen_name']}
        play_df = df[website[site]]
        play_df_csv = play_df.to_csv()
        return play_df_csv

if __name__ == '__main__':
        main()
