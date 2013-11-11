from __future__ import division
from maluuba_napi import client
import csv
import pprint

c=client.NAPIClient('5ald5bubzmX1C8CNp6krpxoOPezui3H2')

# r=c.interpret('Set up a meeting with Bob tomorrow night at 7 PM to discuss the TPS reports')
# r=c.interpret('meet josh at 2')
# http://napi.maluuba.com/v0/interpret?phrase=remind+me+about+my+denist+appointment+tomorrow+at+2&apikey=5ald5bubzmX1C8CNp6krpxoOPezui3H2
# print 'Category', r.category
# print 'Action', r.action
# r.entities

# categories
relevant_intersection_retrieved = 0
retrieved = 0
relevant = 0
#action
relevant_intersection_retrieved_a = 0
retrieved_a = 0
relevant_a = 0

'''
#entities
relevant_intersection_retrieved_e = 0
retrieved_e = 0
relevant_e = 0
'''

results = [['sentence','category','retrieved category','correct','action','retrieved action', 'correct']]

with open('maluuba_test_set_small.csv') as csvfile:
    case_reader = csv.reader(csvfile, delimiter=',')
    for row in case_reader:
        interpreted_sent=c.interpret(row[0])
        # category
        isCorrectCategory = 0
        if interpreted_sent.category is None:
            # failed to retrieve relevant result
            #TODO: include 'KNOWLEDGE' category here
            relevant += 1
        if interpreted_sent.category == row[1]:
            relevant_intersection_retrieved += 1
            retrieved += 1
            relevant += 1
            isCorrectCategory = 1
        else:
            retrieved += 1
        # action
        isCorrectAction = 0
        if interpreted_sent.action is None:
            # failed to retrieve relevant result
            #TODO: include 'KNOWLEDGE_SEARCH' action here
            relevant_a += 1
        if interpreted_sent.action == row[2]:
            relevant_intersection_retrieved_a += 1
            retrieved_a += 1
            relevant_a += 1
            isCorrectAction = 1
        else:
            retrieved_a += 1
        results.append([row[0], row[1], interpreted_sent.category, isCorrectCategory, row[2], interpreted_sent.action, isCorrectAction])
        '''
        # entity
        entities = row[3].split('|')
        retrieved_entities = interpreted_sent.entities
        if interpreted_sent.entities is None:
            if row[1] is None:
                relevant_intersection_retrieved_e += 1
                retrieved_e += 1
                relevant_e += 1
            else:
                relevant_e += 1  
        else:
            for 
            interpreted_sent.entities in :
            relevant_intersection_retrieved_e += 1
            retrieved_e += 1
            relevant_e += 1
        else:
            retrieved_e += 1
        '''
        print '.',

precision = relevant_intersection_retrieved/retrieved
recall = relevant_intersection_retrieved/relevant
precision_a = relevant_intersection_retrieved_a/retrieved_a
recall_a = relevant_intersection_retrieved_a/relevant_a
# precision_e = relevant_intersection_retrieved_e/retrieved_e
# recall_e = relevant_intersection_retrieved_e/relevant_e

print 'Category: Precision',precision,'Recall',recall
print 'Action: Precision',precision_a,'Recall',recall_a
# print 'Entity: Precision',precision_e,'Recall',recall_e

with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(results)
