import argparse

from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report


class EOSClassifier:
    def train(self, trainX, trainY):

        # HINT!!!!!
        # (The following word lists might be very helpful.)
        self.abbrevs = load_wordlist('classes/abbrevs')
        self.sentence_internal = load_wordlist("classes/sentence_internal")
        self.timeterms = load_wordlist("classes/timeterms")
        self.titles = load_wordlist("classes/titles")
        self.unlikely_proper_nouns = load_wordlist("classes/unlikely_proper_nouns")


        # In this part of the code, we're loading a Scikit-Learn model.
        # We're using a DecisionTreeClassifier... it's simple and lets you
        # focus on building good features.
        # Don't start experimenting with other models until you are confident
        # you have reached the scoring upper bound.
        self.clf = DecisionTreeClassifier()  # TODO: experiment with different models
        X = [self.extract_features(x) for x in trainX]
        self.clf.fit(X, trainY)

    def extract_features(self, array):

        # Our model requires some kind of numerical input.
        # It can't handle the sentence as-is, so we need to quantify our them
        # somehow.
        # We've made an array below to help you consider meaningful
        # components of a sentence, for this task.
        # Make sure to use them!
        id, word_m3, word_m2, word_m1, period, word_p1, word_p2, word_3, left_reliable, right_reliable, num_spaces = array

        # The "features" array holds a list of
        # values that should act as predictors.
        # We want to take some component(s) above and "translate" them to a numerical value.
        # For example, our 4th feature has a value of 1 if word_m1 is an abbreviation,
        # and 0 if not.

        features = [  # TODO: add features here
            left_reliable,
            right_reliable,
            num_spaces,
            1 if word_m1 in self.abbrevs else 0

            # ==========TODO==========
            # Make a note of the score you'll get with
            # only the features above (it should be around
            # 0.9). Use this as your baseline.
            # Now, experiment with adding your features.
            # What is a sign that period marks the end of a
            # sentence?
            # Hint: Simpler features will get you further than complex ones, at first.
            # We've given you some features you might want to experiment with below.
            # You should be able to quickly get a score above 0.95!

            # len(word_m1),
            # 1 if word_p1.isupper() else 0
        ]

        return features

    def classify(self, testX):
        X = [self.extract_features(x) for x in testX]
        return self.clf.predict(X)


def load_wordlist(file):
    with open(file) as fin:
        return set([x.strip() for x in fin.readlines()])


def load_data(file):
    with open(file) as fin:
        X = []
        y = []
        for line in fin:
            arr = line.strip().split()
            X.append(arr[1:])
            y.append(arr[0])
        return X, y


def evaluate(outputs, golds):
    correct = 0
    for h, y in zip(outputs, golds):
        if h == y:
            correct += 1
    print(f'{correct} / {len(golds)}  {correct / len(golds)}')


def parseargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', required=True)
    parser.add_argument('--test', required=True)
    parser.add_argument('--output')
    parser.add_argument('--errors')
    parser.add_argument('--report', action='store_true')
    return parser.parse_args()


def main():
    args = parseargs()
    trainX, trainY = load_data(args.train)
    testX, testY = load_data(args.test)

    classifier = EOSClassifier()
    classifier.train(trainX, trainY)
    outputs = classifier.classify(testX)

    if args.output is not None:
        with open(args.output, 'w') as fout:
            for output in outputs:
                print(output, file=fout)

    if args.errors is not None:
        with open(args.errors, 'w') as fout:
            for y, h, x in zip(testY, outputs, testX):
                if y != h:
                    print(y, h, x, sep='\t', file=fout)

    if args.report:
        print(classification_report(testY, outputs))
    else:
        evaluate(outputs, testY)


if __name__ == '__main__':
    main()