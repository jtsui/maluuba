from __future__ import division
from maluuba_napi import client
import csv
import pprint
import progressbar

pr = pprint.PrettyPrinter(indent=2)
# API token requested here http://dev.maluuba.com/
c = client.NAPIClient('5ald5bubzmX1C8CNp6krpxoOPezui3H2')


def pbar(size):
    '''
    Returns a new progress bar
    '''
    bar = progressbar.ProgressBar(maxval=size,
                                  widgets=[progressbar.Bar('=', '[', ']'),
                                           ' ', progressbar.Percentage(),
                                           ' ', progressbar.ETA(),
                                           ' ', progressbar.Counter(),
                                           '/%s' % size])
    return bar


def tag(fin, fout):
    '''
    tag takes strings of input and output files as args
    the input file is a csv with headers sentence, category, and action
    tag iterates through each row in the csv and calls the maluuba API
    to get the actual action and category. the results are stored
    in a list and output as another csv
    '''
    results = []
    with open(fin) as input_file:
        lines = sum(1 for line in input_file)
    bar = pbar(lines - 1)  # for header
    bar.start()
    i = 0
    # headers are sentence, category, action
    with open(fin) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        csv_reader.next()  # skip the header
        for row in csv_reader:
            interpreted_sent = c.interpret(row[0])
            # results have headers sentence, category, retrieved category,
            # action, retrieved action
            results.append(
                [row[0], row[1], interpreted_sent.category, row[2], interpreted_sent.action])
            i += 1
            bar.update(i)
    bar.finish()
    with open(fout, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(results)


def get_precision_recall(results):
    '''
    This is a general function that takes a list of (actual, predicted)
    tuples and returns the recall, precision, and the following rates:
    true positive, false positive, false negative, and true negative
    '''
    tp, fp, fn, tn = 0.0, 0.0, 0.0, 0.0
    for actual, predicted in results:
        if actual == '' and predicted == '':
            tn += 1
        elif actual == '' and predicted != '':
            fn += 1
        elif actual != predicted:
            fp += 1
        elif actual == predicted:
            tp += 1
    return (tp / len(results),  # true positive
            fp / len(results),  # false positive
            fn / len(results),  # false negative
            tn / len(results),  # true negative
            tp / (tp + fn),  # recall
            tp / (tp + fp))  # precision


def evaluate(fin):
    '''
    Evaluate takes the filename of the csv output from tag which has headers
    sentence, category, retrieved category, action, retrieved action.
    It creates slices of the results and prints the statistics including
    precision and recall for each slice.
    '''
    results = []
    with open(fin) as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            results.append(row)
    pad = 30
    title = 'Summary for %s samples' % len(results)
    print title + '\n' + '-' * len(title)
    print ' ' * pad + 'tp\tfp\tfn\ttn\trecall\tprecision\tsamples'
    categories = sorted(list(set([x[1] for x in results])))
    for category_name in categories:
        labels = [(category, retrieved_category)
                  for sentence, category, retrieved_category, action, retrieved_action in results if category == category_name]
        print category_name.ljust(pad) + '%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0f\t' % get_precision_recall(labels) + str(len(labels))
    category_summary = 'category overall'.ljust(pad) + '%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0f' % get_precision_recall(
        [(category, retrieved_category) for sentence, category, retrieved_category, action, retrieved_action in results])
    print '-' * len(category_summary) + '\n' + category_summary + '\n'
    actions = sorted(list(set([x[3] for x in results])))
    for action_name in actions:
        labels = [(action, retrieved_action)
                  for sentence, category, retrieved_category, action, retrieved_action in results if action == action_name]
        print action_name.ljust(pad) + '%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0f\t' % get_precision_recall(labels) + str(len(labels))
    action_summary = 'action overall'.ljust(pad) + '%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0.2f\t%0f' % get_precision_recall(
        [(action, retrieved_action) for sentence, category, retrieved_category, action, retrieved_action in results])
    print '-' * len(action_summary) + '\n' + action_summary + '\n'


def main():
    tag('test_all.csv', 'test_all_output.csv')
    evaluate('test_all_output.csv')

if __name__ == '__main__':
    main()
