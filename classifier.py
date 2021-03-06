import argparse
from itertools import groupby
import re
import numpy as np
from numpy.linalg import norm
from sklearn.tree import DecisionTreeClassifier
from googletrans import Translator
# from google_trans_new import Translator
# from BingTranslator import Translator

client_id = "ClassifierID"
client_secret = "ClassifierSecret"

google_translator = Translator()
# bing_translator = Translator(client_id, client_secret)


class SegmentClassifier:
    def train(self, trainX, trainY):

        self.ru_words = load_wordlist('1000_most_common_russian_words.txt')
        self.uk_words = load_wordlist('1000_most_common_ukrainian_words.txt')

        self.clf = DecisionTreeClassifier()
        X = [self.extract_features(x) for x in trainX]
        self.clf.fit(X, trainY)

    def extract_features(self, text):

        words = text.split()
        features = [
            len(text),
            len(text.strip()),
            len(words),

            # Ukrainian
            # Cyrillic letter GJE
            1 if re.search('[\u0453]', text) == 1 or re.search(
                '[\u0403]', text) == 1 else 0,
            # Cyrillic letter IE
            1 if re.search('[\u0454]', text) == 1 or re.search(
                '[\u0404]', text) == 1 else 0,
            # Cyrillic letter YI
            1 if re.search('[\u0407]', text) == 1 or re.search(
                '[\u0457]', text) == 1 else 0,
            # Cyrillic letter Byelorussian-Ukrainian I
            1 if re.search('[\u0456]', text) == 1 or re.search(
                '[\u0406]', text) == 1 else 0,

            1 if sum(
                1 if word in self.uk_words else 0 for word in words) > 1 else 0,
            3 if sum(
                1 if word in self.uk_words else 0 for word in words) > 5 else 0,
            5 if sum(
                1 if word in self.uk_words else 0 for word in words) > 10 else 0,

            # Russian
            # Cyrillic letter IO
            1 if re.search('[\u0451]', text) == 1 or re.search(
                '[\u0401]', text) == 1 else 0,
            # Cyrillic letter HARD SIGN
            1 if re.search('[\u044A]', text) == 1 or re.search(
                '[\u042A]', text) == 1 else 0,
            # Cyrillic letter YERU
            1 if re.search('[\u042B]', text) == 1 or re.search(
                '[\u044B]', text) == 1 else 0,
            # Cyrillic letter E
            1 if re.search('[\u044D]', text) == 1 or re.search(
                '[\u042D]', text) == 1 else 0,

            1 if sum(
                1 if word in self.ru_words else 0 for word in words) > 1 else 0,
            3 if sum(
                1 if word in self.ru_words else 0 for word in words) > 5 else 0,
            5 if sum(
                1 if word in self.uk_words else 0 for word in words) > 10 else 0,
        ]
        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)


def load_wordlist(file):
    with open(file) as fin:
        return set([x.strip() for x in fin.readlines()])


def load_data(file, ru_dics, uk_dics):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split('\t', 1)
            if arr[0] == '#BLANK#':
                continue
            X.append(arr[1])  # text
            y.append(arr[0])  # classification

            # Fill ru and uk dics
            if arr[0] == 'uk' or arr[0] == '"uk':
                temp_dict = tf(arr[1])
                uk_dics.append(temp_dict)
            else:
                temp_dict = tf(arr[1])
                ru_dics.append(temp_dict)
        return X, y


def lines2segments(trainX, trainY):
    segX = []
    segY = []
    for y, group in groupby(zip(trainX, trainY), key=lambda x: x[1]):
        if y == '#BLANK#':
            continue
        x = '\n'.join(line[0].rstrip('\n') for line in group)
        segX.append(x)
        segY.append(y)
    return segX, segY


def evaluate(outputs, golds):
    correct = 0
    for h, y in zip(outputs, golds):
        if h == y:
            correct += 1
    print(f'{correct} / {len(golds)}  {correct / len(golds)}')


def parseargs():
    parser = argparse.ArgumentParser()
    # Train tweets to be passed everytime
    parser.add_argument('--train', required=True)
    parser.add_argument('--test', required=True)  # New text to be judged
    parser.add_argument('--format', required=False)
    parser.add_argument('--output')
    parser.add_argument('--errors')
    parser.add_argument('--report', action='store_true')
    return parser.parse_args()


def dictdot(x, y):
    # Function to compute dot product of two vectors

    keys = list(x.keys()) if len(x) < len(y) else list(y.keys())
    return sum(x.get(key, 0) * y.get(key, 0) for key in keys)


def cosine_sim(x, y):
    # Function to compute cosine similarity

    num = dictdot(x, y)
    if num == 0:
        return 0
    return num / (norm(list(x.values())) * norm(list(y.values())))


def tf(sent):
    # Function to compute tf

    dic = {}
    x = sent.split()
    for word in x:
        if word in dic:
            dic[word] += 1
        else:
            dic[word] = 1

    return dic


def main():
    args = parseargs()

    # Process development data
    #args.train = './input_data-train.tsv'
    #args.format = line

    ru_dics = []
    uk_dics = []
    trainX, trainY = load_data(args.train, ru_dics, uk_dics)
    # print(ru_dics)
    # print(uk_dics)
    # exit()

    # Processing test phrase
    testX = []
    testX.append(args.test)
    testY = []
    testY.append('Unkown')

    test_dict = tf(args.test)

    # Format for testing

    if args.format == 'segment':
        trainX, trainY = lines2segments(trainX, trainY)
        testX, testY = lines2segments(testX, testY)

    classifier = SegmentClassifier()
    classifier.train(trainX, trainY)
    outputs = classifier.classify(testX)

    # Computing similarity
    # Computing similarity to ukrainian train data
    uk_cosine_sum = 0
    ru_cosine_sum = 0
    for sent in uk_dics:
        uk_cosine_sum += cosine_sim(sent, test_dict)
    for sent in ru_dics:
        ru_cosine_sum += cosine_sim(sent, test_dict)

    uk_cosine = uk_cosine_sum/len(uk_dics)
    ru_cosine = ru_cosine_sum/len(ru_dics)

    # Computing similarity to russain train data

    for truth, output, text in zip(testY, outputs, testX):
        #print('This is the text you passed: ')
        #print('         ' + text)
        print('\nDecision Tree classification:')
        if output == '"uk':
            print('\t\tUkrainian')
        else:
            print('\t\tRussian')
        print('\nCosine similarity classification:')
        if uk_cosine > ru_cosine:
            print('\t\tUkrainian')
        else:
            print('\t\tRussian')
        print('\nCosine similarity to Ukrainian: ' + "{:.6f}".format(uk_cosine))
        print('Cosine similarity to Russian: ' +  "{:.6f}".format(ru_cosine))

        print('\nGoogle Translate classification:')
        google_result = google_translator.translate(text)
        print('\t\t' + google_result.src)
        print('\nTranslation:')
        print('\t\t' + google_result.text)

        # Bing translation
        '''
        bing_detection = bing_translator.detect_language(text)
        bing_result = bing_translator.translate(text, "pt")
        print('Bing translate believes the langauge of the text you have passed is: ')
        print('         ' + bing_detection)
        print('AND this is the translation of your text by Bing translate: ')
        print('         ' + bring_result)
        '''

    """
    if args.errors is not None:
        with open(args.errors, 'w') as fout:
            for y, h, x in zip(testY, outputs, testX):
                if y != h:
                    print(y, h, x, sep='\t', file=fout)

    if args.report:
        print(classification_report(testY, outputs))
    else:
        evaluate(outputs, testY)
    """


if __name__ == '__main__':
    main()
