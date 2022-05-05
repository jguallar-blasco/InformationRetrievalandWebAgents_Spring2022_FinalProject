import tweepy as tw
import time
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

    query = 'Tweepy -lang:' + lang
    response = client.get_recent_tweets_count(query, granularity='day')

    tweet_count = 0
    for count in response.data:
        tweet_count += count['tweet_count']

    return tweet_count


def extract_tweeps(client, lang):
    '''Extract any Tweets from past week
    where given language requirement is met.'''

    query = 'Tweepy -lang:' + lang
    response = client.get_recent_tweets_count(query, granularity='day')

    # Creation of dataframe from tweets list
    # Add or remove columns as you remove tweet information
    tweets_df = pd.DataFrame(tweets_list)
    path = 'uk.csv'
    tweets_df.to_csv(path, index=False)

    try:
        # Creation of query method using parameters
        tweets = tw.API.search_tweets(q='', lang=l, count=c)

        # Pulling information from tweets iterable object
        tweets_list = [[tweet.lang, tweet.text]
                       for tweet in tweets]

        # Creation of dataframe from tweets list
        # Add or remove columns as you remove tweet information
        tweets_df = pd.DataFrame(tweets_list)
        path = l + '.csv'
        tweets_df.to_csv(path, index=False)
        return tweets_df

    except BaseException as e:
        print('failed on_status,', str(e))
        time.sleep(3)


def format_input():
    '''Use exported Tweets and mix together
    randomly to create input dataset.'''

    return


def main():

    client = oauth_tweepy()

    tweets = []

    tweets.append(extract_tweeps(client, 'ru'))
    tweets.append(extract_tweeps(client, 'uk'))

    return
    format_input(tweets)


if __name__ == '__main__':
    main()
