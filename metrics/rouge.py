import os
from utilities import read_files
import csv
import pandas as pd
import sys
import pickle
import copy

def get_ground_truth(file):
    name = file.split("/")[-1].split("_")[0]
    return [f for f in ground_truth if name in f][0]

def precision_metric_unigram(response, ground_truth):
    response = response.split(" ")
    ground_truth = ground_truth.split(" ")
    try:
        return len(set(response).intersection(set(ground_truth))) / len(response)
    except:
        return 0.0

def recall_metric_unigram(response, ground_truth):
    response = response.split(" ")
    ground_truth = ground_truth.split(" ")
    try:
        return len(set(response).intersection(set(ground_truth))) / len(ground_truth)
    except:
        return 0.0
    
def f1_metric_unigram(response, ground_truth):
    precision = precision_metric_unigram(response, ground_truth)
    recall = recall_metric_unigram(response, ground_truth)
    try:
        return 2 * (precision * recall) / (precision + recall)
    except:
        return 0.0
    
def intersection_ngrams(response, ground_truth, n):
    response = response.split(" ")
    ground_truth = ground_truth.split(" ")
    response_ngrams = [" ".join(response[i:i+n]) for i in range(len(response)-n+1)]
    ground_truth_ngrams = [" ".join(ground_truth[i:i+n]) for i in range(len(ground_truth)-n+1)]
    return response_ngrams, ground_truth_ngrams

def precision_ngrams(response, ground_truth, n):
    response_ngrams, ground_truth_ngrams = intersection_ngrams(response, ground_truth, n)
    try:
        return len(set(response_ngrams).intersection(set(ground_truth_ngrams))) / len(response_ngrams)
    except:
        return 0.0
    
def recall_ngrams(response, ground_truth, n):
    response_ngrams, ground_truth_ngrams = intersection_ngrams(response, ground_truth, n)
    try:
        return len(set(response_ngrams).intersection(set(ground_truth_ngrams))) / len(ground_truth_ngrams)
    except:
        return 0.0
    
def f1_ngrams(response, ground_truth, n):
    precision = precision_ngrams(response, ground_truth, n)
    recall = recall_ngrams(response, ground_truth, n)
    try:
        return 2 * (precision * recall) / (precision + recall)
    except:
        return 0.0
    
def get_all_combinations(text):
    text = text.split(" ")
    all_combinations = []
    for i in range(len(text)):
        all_combinations.append([text[i]])
        for j in range(i+1, len(text)):
            combination = [text[k] for k in range(i, j)] + [text[j]]
            all_combinations.append(combination)
            for k in range(j+1, len(text)):
                combination = [text[r] for r in range(i, j+1)] + [text[k]] 
                all_combinations.append(combination)
    
    unique = [list(comb) for comb in set([tuple(comb) for comb in all_combinations])]
    return unique

def intersection_LCS(ngrams_response, ngrams_ground_truth):
    count = []
    for item in ngrams_response:
        if item in ngrams_ground_truth:
            count.append(item)
    return max(count, key=len)

def precision_ngrams_nonconsecutive(response, ground_truth):
    response_ngrams = get_all_combinations(response)
    ground_truth_ngrams = get_all_combinations(ground_truth)
    try:
        return len(intersection_LCS(response_ngrams, ground_truth_ngrams)) / len(response.split(" "))
    except:
        return 0.0
    
def recall_ngrams_nonconsecutive(response, ground_truth):
    response_ngrams = get_all_combinations(response)
    ground_truth_ngrams = get_all_combinations(ground_truth)
    try:
        return len(intersection_LCS(response_ngrams, ground_truth_ngrams)) / len(ground_truth.split(" "))
    except:
        return 0.0
    
def f1_ngrams_nonconsecutive(response, ground_truth, ngrams=0):
    precision = precision_ngrams_nonconsecutive(response, ground_truth)
    recall = recall_ngrams_nonconsecutive(response, ground_truth)
    try:
        return 2 * (precision * recall) / (precision + recall)
    except:
        return 0.0
    
def run_results(files, results_dict, metric, ngrams=1):
    dict_ = copy.deepcopy(results_dict)
    for file in files:
            gd = open(get_ground_truth(file)).read()
            text = open(file).read()
            result = metric(text, gd, ngrams)
            if "cluster" in file:
                dict_["cluster"].append((file, result))
            else:
                dict_["folder"].append((file, result))
    return dict_


models = os.listdir("./results")
ground_truth = read_files("./data/examples")
ground_truth = [file for file in ground_truth if file.endswith(".sysml")]


for model in models:
    files = read_files(f"./results/{model}")
    results_ = {
        "cluster" : [],
        "folder" : []
    }        
    for i in range(1, 4):
        rouge_score = run_results(files, results_, f1_ngrams, i)
        with open(f"metrics/{model}_rouge_{i}.pkl", "wb") as out:
            pickle.dump(rouge_score, out)
    
    # rouge_lcs = run_results(files, results_, f1_ngrams_nonconsecutive, 0)
    # with open(f"metrics/{model}_rouge_lcs", "wb") as out:
    #     pickle.dump(rouge_lcs, out)

