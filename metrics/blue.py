import pickle
from utilities import read_files
import copy
import os 
from math import exp

def get_ground_truth(file):
    name = file.split("/")[-1].split("_")[0]
    return [f for f in ground_truth if name in f][0]

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

def mean_blue(response, ground_truth, n):
    vals = []
    for i in range(1, n+1):
        vals.append(precision_ngrams(response, ground_truth, i))

    return sum(vals)/len(vals)

def blue_score(response, ground_truth, bp, n):
    mean_blue_score = mean_blue(response, ground_truth, n)
    return mean_blue_score * bp

def run_results(files, results_dict, metric):
    dict_ = copy.deepcopy(results_dict)
    for file in files:
            gd = open(get_ground_truth(file)).read()
            text = open(file).read()
            if len(text) > len(gd):
                bp = 1.0
            else:
                try:
                    bp = exp(1 - len(gd) / len(text))
                except:
                    bp = 0.0
            result = metric(text, gd, bp, 4)
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
    bleu_ = run_results(files, results_, blue_score)
    with open(f"metrics/{model}_bleu.pkl", "wb") as out:
        pickle.dump(bleu_, out)