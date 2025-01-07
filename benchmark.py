import litellm
from utilities import read_files
import ollama
import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import time
import pickle

# In case of remote use, sometimes the environement variable doesn't load so the API Key has to be set manually.
API_KEY = "___________________________________________________________________________" 
CONTEXT_MAX = 9000

def get_examples_folder(file):
    '''
    Function to get examples from the same folder as the working file.
    :param file: file path
    :return: list of examples from the same folder, capped at 3.
    '''
    dir = "/".join(file.split("/")[:-1])
    examples = [f"{dir}/{f}" for f in os.listdir(dir) if f.endswith('.sysml') and f != file.split("/")[-1]]
    if len(examples) > 3:
        return np.random.choice(examples, 3, replace=False)
    else:
        return examples

def get_examples_clusters(file):
    '''
    Function to get examples from the same cluster as the working file.
    :param file: file path
    :return: list of examples from the same cluster, capped at 3.
    '''
    # to gain time in the process, we load the embeddings from a pickle file
    df = pd.read_pickle("embeddings/df_text_embedding_large.pkl")
    
    cluster = df[df["file"] == file]["kmeans_labels"].values[0]
    df = df.drop(df[df["file"] == file].index)
    examples = df[df["kmeans_labels"] == cluster]["file"].values
    
    if len(examples) > 3:
        return np.random.choice(examples, 3, replace=False)
    else:
        return examples

def generate_mode(mode, model, model_name):
    '''
    Function to generate the code for a given file and mode.
    :param mode: mode to use, either "cluster" or "folder"
    :param model: model to use
    :param model_name: model name
    
    :return: None
    '''
    
    # file name is the name of the file without the path and the extension
    file_name = file.split("/")[-1].replace(".sysml", "")
    
    if mode == "cluster":
        examples = examples_dict[file]["cluster"]
    else:
        examples = examples_dict[file]["folder"]
    
    # deep copy of the template prompt to avoid overwriting
    prompt = template_prompt.copy()
    
    text_content = open(f"prompts/{file.split('/')[-1].replace('.sysml', '.txt')}").read()
    
    prompt[0]['content'] += "\n".join([f"Example {i+1} : \n{open(f).read()}\n" for i, f in enumerate(examples)])
    prompt[1]["content"] = f"Generate the code in SysMLV2 for the following description : \n{text_content}\n Output the code only and nothing else."
    
    # Some models have context length limitations, so we cap it to a maximum value
    if len(prompt[1]["content"]) > CONTEXT_MAX:
        prompt[1]["content"] = prompt[1]["content"][:CONTEXT_MAX]
    
    
    response = litellm.completion(model=model, messages=prompt, api_key=API_KEY)
    response = response["choices"][0]["message"]["content"]
    
    if not os.path.exists(f"results/{model_name}"):
        # create directory for model responses if it doesn't exist
        os.makedirs(f"results/{model_name}")
    
    with open(f"results/{model_name}/{file_name}_{mode}.txt", "w") as f:
            f.write(response)

######## FILES LOAD
files = read_files("./data/examples")
print("files read")

# models to use
models = [f"ollama/{model.model}" for model in ollama.list()["models"]] +  ["openai/gpt-4-turbo", "openai/gpt-3.5-turbo"] 

###### TEMPLATE PROMPT
template_prompt = [
    {
        "role" : "system",
        "content" : "You are a SysMLV2 Engineer. You are given a description of a model and you have to generate the code in SysMLV2. You should output the code only and nothing else. Here are some examples : \n"
    },
    {
        "role" : "user",
        "content" : ""
    }
]

#### Create dict to facilitate processing (not redo the same process each time)

examples_dict = {}
for file in files:
    examples_folder = get_examples_folder(file)
    examples_cluster = get_examples_clusters(file)
    
    examples_dict[file] = {
        "folder" : get_examples_folder(file),
        "cluster" : get_examples_clusters(file)
    }
    
    
time_dict = {model : [] for model in models}

for model in models:
    model_name = model.split("/")[-1].replace(":", "_")
    print(f"Generating for model : {model_name}")
    for file in files:
        print(f"processing {file}")
        if not os.path.exists(f"results/{model_name}/{file.split('/')[-1].replace('.sysml', '')}_cluster.txt"):
            start = time.time()
            generate_mode("cluster", model, model_name)
            time_ = time.time() - start
            time_dict[model].append(("cluster", file, time_)) 
        if not os.path.exists(f"results/{model_name}/{file.split('/')[-1].replace('.sysml', '')}_folder.txt"):
            start = time.time()
            generate_mode("folder", model, model_name)
            time_ = time.time() - start
            time_dict[model]= [("folder", file, time_)]
            
with(open("time_dict.pkl", "wb")) as f:
    pickle.dump(time_dict, f, protocol=pickle.HIGHEST_PROTOCOL)