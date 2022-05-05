from sklearn.metrics import jaccard_score
import twint


def extract_information(lang):
    '''Extract short Tweets information where
    language is the one specified by the argument.'''

    c = twint.Config()
    # c.Username = "noneprivacy"
    c.Limit = 50
    c.Store_csv = True
    c.Since = 2022
    c.Output = lang + '.csv'
    c.Pandas = True
    c.Lang = lang
    twint.run.Search(c)

    results = twint.storage.panda.Tweets_df
    return results


def format_input():
    '''Use exported Tweets and mix together
    randomly to create input dataset.'''

    return


def main():

    langs = ['ru', 'ru-RU', 'uk', 'uk-UA']

    for l in langs:
        extract_information(l)


if __name__ == '__main__':
    main()
