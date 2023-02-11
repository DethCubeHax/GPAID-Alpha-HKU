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

from transformers import pipeline


MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
# config = AutoConfig.from_pretrained(MODEL)

model = AutoModelForSequenceClassification.from_pretrained(MODEL)


sia = SentimentIntensityAnalyzer()


#roberta model running function
def polarity_scores_roberta(id,example):
    encoded_text = tokenizer(example, return_tensors='pt')
    output = model(**encoded_text)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    scores_dict = {
        'roberta_neg' : scores[0],
        'roberta_neu' : scores[1],
        'roberta_pos' : scores[2],
        'rev' : example
    }
    return scores_dict


import json 
index = 0
dictionary_ult = {}        
with open ("ACCT1101.txt") as f:
    for line in f:
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
            res[index2] = polarity_scores_roberta(index2,text)
            index2 += 1
        
        except RuntimeError:
            print(f"Broke for id {index2}")
        
    # break
    
results_df = pd.DataFrame(res).T
results_df = results_df.sort_values('roberta_pos',ascending=False)
results_df.to_csv("output1.csv")
# print(res)

        







