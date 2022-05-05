import twint
import tweepy as tw
import time
import pandas as pd


def oauth_tweepy():
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


def extract_tweeps(client, language):
    l = language
    c = 5000

    query = 'Tweepy -lang:' + language
    response = client.get_recent_tweets_count(query, granularity='day')

    tcount = 0
    for count in response.data:
        tcount += count['tweet_count']

    print(tcount)

    return
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


def extract_tweets(lang):
    '''Extract short Tweets information where
    language is the one specified by the argument.'''

    c = twint.Config()

    # Extract only Tweets with specified
    # language

    c.Lang = lang

    # Search only for short tweets in last year
    # to limit size of data

    # c.Limit = 10
    # c.Year = '2019'
    # c.Since = '2022-01-01'

    # c.Search = 'from:@JHUBME'
    # c.Store_csv = True
    # c.Output = lang + '.csv'

    # c.Pandas = True

    twint.run.Search(c)

    # results = twint.storage.panda.Tweets_df
    # print(results)
    # return results


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
