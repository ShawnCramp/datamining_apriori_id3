""" ---------------------------------------------------------
Author: Shawn Cramp
ID: 111007290
Author: Omar Farah
ID:
Author: Nick Hare
ID:
Description: CP465 Final Assignment
Date: October, 28th, 2016
-------------------------------------------------------------
Assignment Task:
The objective of this project is to implement two Data Mining
algorithms and test your implementations with various reasonably
large datasets. The term reasonably large is to be interpreted
as anywhere from a few hundreds to a few thousands instances (tuples).

You need to implement two Data Mining algorithms seen in class:
1. the ID3 algorithm, based on entropy/information gain, to build decision trees;
2. the Apriori algorithm for mining association rules;

-------------------------------------------------------------
Import Declarations ------------------------------------- """


""" ---------------------------------------------------------
Global Declarations ------------------------------------- """


""" ---------------------------------------------------------
Class Declarations -------------------------------------- """

from sys import argv
from operator import itemgetter
import urllib2
import csv

def print_list(list):
    for l in list:
        print "[ {0} ]".format(l)

def print_support(support):
    for s in support:
        print "[ {0} = {1} ]".format(s, support[s])

def print_freq_items(sets, support):
    for ss in sets:
        for s in ss:
            print "Frequent set: {{ {0} }}, support: {1:.2f}".format(", ".join(s), support[s])

def print_freq_items_tofile(sets, support):
    f = open('supportlist.txt', 'w')
    for ss in sets:
        for s in ss:
            f.write("Frequent set: {{ {0} }}, support: {1:.2f}\n".format(", ".join(s), support[s]))
    f.close()

def print_rules(rules):
    for rule in rules:
        print "{{ {0} }} --> {{ {1} }}, conf: {2:.2f}".format(", ".join(rule[0]), ", ".join(rule[1]), rule[2])

def print_rules_tofile(rules):
    f = open('output.txt', 'w')
    for rule in rules:
        f.write("{{ {0} }} --> {{ {1} }}, conf: {2:.2f} \n".format(", ".join(rule[0]), ", ".join(rule[1]), rule[2]))
    f.close()

def apriori(data, min_sup=0.3):
    single_candidates = get_single_candidates(data)
    #print "Single Candidates" #DEBUG
    #print_list(single_candidates) #DEBUG
    datasets = map(set, data)
    frequent_singles, sup_cnts = prune_by_support(datasets, single_candidates, min_sup)
    #print "Freq Item Sets" #DEBUG
    #print_list(frequent_singles) #DEBUG
    #print "Supports " #DEBUG
    #print_support(sup_cnts) #DEBUG
    frequent_sets = []
    frequent_sets.append(frequent_singles)
    k = 0
    while(len(frequent_sets[k]) > 0):
        candidates = get_candidates(frequent_sets[k])
        #print "{0} iter".format(k) #DEBUG
        #print "Candidates: " #DEBUG
        #print_list(candidates) #DEBUG
        freq_k_sets, sup_k_cnts = prune_by_support(datasets, candidates, min_sup)
        #print "Freq Sets:" #DEBUG
        #print_list(freq_k_sets) #DEBUG
        #print "Supports: " #DEBUG
        #print_support(sup_k_cnts) #DEBUG
        sup_cnts.update(sup_k_cnts)
        frequent_sets.append(freq_k_sets)
        k += 1
    return frequent_sets, sup_cnts

def get_single_candidates(dataset):
    single_candidates = []
    for transaction in dataset:
        for item in transaction:
            c = [item]
            if not c in single_candidates:
                single_candidates.append(c)

    single_candidates.sort()
    return map(frozenset, single_candidates)

def get_candidates(frequent_sets):
    ret_frequent = []
    freq_len = len(frequent_sets)
    #print "get_candidates : freq_sets = {0}, len = {1}".format(frequent_sets, freq_len)
    for i in range(freq_len):
        for j in range(i+1, freq_len):
            fli = list(frequent_sets[i])
            fli.sort()
            #print "fli: {0}, {1}".format(fli, i)
            flj = list(frequent_sets[j])
            flj.sort()
            #print "flj: {0}, {1}".format(flj, j)
            if (len(fli) < 2):
                fsi = fli[0]
                fsj = flj[0]
                #print "fsi == fsj : {0} == {1}".format(fsi, fsj)
                ret_frequent.append(frequent_sets[i] | frequent_sets[j])
            else:
                fsi = fli[:-1]
                fsj = flj[:-1]
                #print "fsi == fsj : {0} == {1}".format(fsi, fsj)
                if fsi == fsj:
                    ret_frequent.append(frequent_sets[i] | frequent_sets[j])
    return ret_frequent

def prune_by_support(datasets, candidates, min_sup):
    items_cnts = {}
    data_len = float(len(datasets))
    prunned_items = []
    support_cnts = {}
    for transaction in datasets:
        for candidate in candidates:
            if candidate.issubset(transaction):
                items_cnts.setdefault(candidate, 0)
                items_cnts[candidate] += 1

    for candidate_set in items_cnts:
        support = items_cnts[candidate_set] / data_len
        if support >= min_sup:
            prunned_items.append(candidate_set)
        support_cnts[candidate_set] = support

    return prunned_items, support_cnts

def get_candidate_rules(frequent_sets):
    ret_frequent = []
    freq_len = len(frequent_sets)
    #print "get_candidates : freq_sets = {0}, len = {1}".format(frequent_sets, freq_len)
    for i in range(freq_len):
        for j in range(i+1, freq_len):
            fli = list(frequent_sets[i])
            fli.sort()
            #print "fli: {0}, {1}".format(fli, i)
            flj = list(frequent_sets[j])
            flj.sort()
            #print "flj: {0}, {1}".format(flj, j)
            if (len(fli) < 2):
                fsi = fli[0]
                fsj = flj[0]
                #print "fsi == fsj : {0} == {1}".format(fsi, fsj)
                ret_frequent.append(frequent_sets[i] | frequent_sets[j])
            else:
                fsi = fli[:-1]
                fsj = flj[:-1]
                #print "fsi == fsj : {0} == {1}".format(fsi, fsj)
                if fsi == fsj:
                    ret_frequent.append(frequent_sets[i] | frequent_sets[j])
    return ret_frequent

def generate_rules(f_set, Hm, sup_cnts, min_conf, rules):
    k = len(f_set)
    m = len(Hm[0])
    if (k > m + 1):
        Hm1 = get_candidate_rules(Hm)
        prune_by_confidence(f_set, Hm1, sup_cnts, min_conf, rules)
        #print "Pruned rules: {0}:".format(Hm1)
        if len(Hm1) > 1:
            generate_rules(f_set, Hm1, sup_cnts, min_conf, rules)

def prune_by_confidence(f_set, H, sup_cnts, min_conf, rules):
    for consequence in H:
        rule = f_set - consequence
        confidence = sup_cnts[f_set] / sup_cnts[rule]
        if confidence >= min_conf:
            #print "** Rule: {0} \nconsequence: {1}\n confidence: {2}".format(rule, consequence, confidence)
            rules.append((rule, consequence, confidence))
    
def get_rules(f, sup_cnts, min_conf = 0.6):
    rules = []
    for i in range(1, len(f)):
        for f_set in f[i]:
            Hm = [frozenset([itemset]) for itemset in f_set]
            generate_rules(f_set, Hm, sup_cnts, min_conf, rules)
    #print rules
    return rules

if __name__ == '__main__':
    with open("trim.txt", "r") as file:
        data = [[x for x in line.strip().split(",")] for line in file]
    print(data)
    min_sup = .3
    min_conf = .6

    frequent_sets, sup_cnts = apriori(data, min_sup)
    frequent_sets = frequent_sets[:-1]
    #print "Final Frequent Sets:"
    #print_list(frequent_sets)
    #print_support(sup_cnts)
    print_freq_items_tofile(frequent_sets, sup_cnts)
    rules = get_rules(frequent_sets, sup_cnts, min_conf)
    #print "Rules: "
    rules.sort(key = itemgetter(2), reverse=True)
    print_rules_tofile(rules)
