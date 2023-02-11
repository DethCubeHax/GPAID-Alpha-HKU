# Import the required libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
from scipy.special import softmax
import string
import json

#pre-trained model being used for sentiment-analysis
MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
#token for model model training
tokenizer = AutoTokenizer.from_pretrained(MODEL)
# config = AutoConfig.from_pretrained(MODEL)
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
sia = SentimentIntensityAnalyzer()

#roberta model running function
def polarity_scores_roberta(example):
    #form an encoded version of the text using pytorch
    encoded_text = tokenizer(example, return_tensors='pt')
    #inject the encoded text into the model to output result
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    scores_dict = {
        'roberta_neg' : scores[0],
        'robserta_neu' : scores[1],
        'roberta_pos' : scores[2],
        'rev' : example
    }
    return scores_dict


# Define the location of the directory
#path =r"/Users/wasiflatifhussain/Documents/Projects_Nafis/tester-rev"
# print(os.chdir)
root_path=os.getcwd()
path =f"{root_path}/tester-rev"
# Change the directory
os.chdir(path)

def read_files(file_path,file_name):
    index = 0
    dictionary_ult = {}
    with open(file_path, 'r') as file:
    #   print(file.read())
        for line in file:
            js = json.loads(line[:-2:])
            for key in js:
                if (key == "content"):
                    dictionary_ult[index] = js[key]
                    index += 1
        
    res = {}
    index2 = 0
    for key in dictionary_ult:
        if (dictionary_ult[key] != None):
            try:
                text = str(dictionary_ult[key])
                text = text.translate(str.maketrans('','',string.punctuation))
                res[index2] = polarity_scores_roberta(text)
                index2 += 1
            
            except RuntimeError:
                print(f"Broke for id {index2}")
    results_df = pd.DataFrame(res).T
    
    print(results_df.empty)
    file_name2=file_name[:len(file_name)-4]
    print(file_name2)
    if (results_df.empty == False):
        results_df = results_df.sort_values('roberta_pos',ascending=False)
        results_df.to_csv(f"{root_path}/results/{file_name2}.csv")
    elif (results_df.empty == True):
        results_df.to_csv(f"{root_path}/results/{file_name2}.csv")
# Iterate over all the files in the directory
for file in os.listdir():
   if file.endswith('.txt'):
      # Create the filepath of particular file
      file_path =f"{path}/{file}"

      read_files(file_path,file)