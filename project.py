import sys
import time
import tweepy as tw
import pandas as pd


def oauth_tweepy():
    '''Authenticate Twitter API v2 Client
    to allow Tweepy to scrape data.'''

    consumer_key = "EMdB9fj1AX12HDKicRX8AYwoV"
    consumer_secret = "7VdJSlDif7r7urcBf2Wtaya2gUCP2pthF6JbEG6ptQjshacMcm"
    access_token = "1362869631468380161-Hu4sMV946cMSCBaeOq6Ar0DIqthopG-B9Evwp0Iyb7kHKVO3TTfOjOo2Tputk"
    access_token_secret = "TboxTxWNMBXtTgBrZpeSFlFRP7GpKo6aMbjStgjvqgbP9"
    bearer_token = "AAAAAAAAAAAAAAAAAAAAAFQKcQEAAAAA2HmR5DGzrfkLA5XnD%2FXPPQELjP0%3Di26C8qlQnaSmLDkcnYnyfqQhAmrpoea7DJKoKTumv7rURiqYJa"

    # client = tw.Client(
    #     consumer_key=consumer_key,
    #     consumer_secret=consumer_secret,
    #     access_token=access_token,
    #     access_token_secret=access_token_secret
    # )

    client = tw.Client(
        bearer_token=bearer_token
    )

    return client


def extract_tweet_count(client, lang):
    '''Extract number of Tweets from past week
    where given language requirement is met.'''

    query = 'kyiv -lang:' + lang
    response = client.get_recent_tweets_count(query, granularity='hour')

    tweet_count = 0
    starts = []
    ends = []

    for count in response.data:
        # tweet_count += count['tweet_count']
        tweet_count += 100
        starts.append(count['start'])
        ends.append(count['end'])

        if tweet_count >= 5000:
            break

    return tweet_count, [starts, ends]


def extract_tweets(client, lang, time_list):
    '''Extract any Tweets from past week
    where given language requirement is met.'''

    query = 'kyiv -lang:' + lang
    tweets_list = []

    for i in range(1, len(time_list)):
        try:
            s = time_list[0][i]
            e = time_list[1][i]

            response = client.search_recent_tweets(
                query, max_results=100, start_time=s, end_time=e)
            # The method returns a Response object, a named tuple with data, includes,
            # errors, and meta fields

            # In this case, the data field of the Response returned is a list of Tweet
            # objects
            tweets = response.data

            # Pulling information from tweets iterable object
            tweets_list_small = [[tweet.lang, tweet.text]
                                 for tweet in tweets]

            tweets_list.extend(tweets_list_small)

        except BaseException as e:
            print('failed on_status,', str(e))
            time.sleep(3)

    tweets_df = pd.DataFrame(tweets_list)
    output_tweets(tweets_df, lang)

    return tweets_df


def output_tweets(df, name):
    '''Export extracted tweets from
    a given language as a .csv file.'''

    path = name + '.csv'
    df.to_csv(path, index=False)


def format_input(df_list):
    '''Use exported Tweets and mix together
    randomly to create input dataset.'''

    shuffle = pd.concat(df_list).sample(frac=1)

    output_tweets(shuffle, 'input_data')


def main():
    args = len(sys.argv)

    if args == 2 and sys.argv[1] == 'extract':
        client = oauth_tweepy()

        df_list = []
        times_lists = []

        for l in ['uk', 'ru']:
            count, time_list = extract_tweet_count(client, l)
            print(l, ': ', count)
            times_lists.append(time_list)

        df_list.append(extract_tweets(client, 'uk', times_lists[0]))
        df_list.append(extract_tweets(client, 'ru', times_lists[1]))

        format_input(df_list)

    elif args == 3:
        uk = sys.argv[1]
        ru = sys.argv[2]

        df_list = []
        df_list.append(pd.read_csv(uk + '.csv', index_col=False))
        df_list.append(pd.read_csv(ru + '.csv', index_col=False))

        format_input(df_list)

    else:
        print('\nUsage is:\n')
        print('\t python project.py extract')
        print('\t to extract Tweets from python and write to .csv as well as format\n')
        print('\t python project.py uk-data ru-data')
        print('\t to read from existing .csv as well as format\n')


if __name__ == '__main__':
    main()
