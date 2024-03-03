import pandas as pd 
import numpy as np 

corpus2 = pd.read_csv("Corpus2.csv")
corpus = pd.read_csv("Corpus.csv")




def get_values(result,touken=False):
    allx = []
    new_values = []
    
    for x in result[1:]:
        if x is not np.nan:
            value ,freq= x.split("|")
            new_values.append([int(freq),value])
    return new_values

def get_probibilties(possiblities:list[str],threshold=0.1):
    total = 0
    probs = []
    new_possiblities = []
    for pos in possiblities :
        total+=pos[0]
    for i,pos in enumerate(possiblities) :
        new_possiblities.append([pos[0]/total,pos[1]])
        probs.append(pos[0]/total)
    
    if all(prob >threshold for prob in probs) :
        return new_possiblities
    else :
        possiblities = [possiblities[i] for i,prob in enumerate(probs) if prob > threshold]
        return get_probibilties(possiblities,threshold=threshold)

def sample_distrubtion(probs):
    probilities , values = zip(*probs)

    ran_value = np.random.choice(values,p=probilities)

    return ran_value

def reccomand(text:str,thershold=0.1,by_sentences = True):
    if not by_sentences :
        word = text.split(" ")
        word = word[-1]
        result = corpus.loc[corpus["name"]==word].squeeze()
        

        
    else :
        word = text.split(" ")
        word = " ".join(word[-2:])
        print(word)
        if corpus2['name'].isin([word]).any():
            result = corpus2.loc[corpus2["name"]==word].squeeze()
            
            
        else :
            
            result = corpus.loc[corpus["name"]==word].squeeze()
            
            word = text.split(" ")
            word = word[-1]
            result = corpus.loc[corpus["name"]==word].squeeze()

    result = get_values(result)
    probs = get_probibilties(result,threshold=thershold)
    recomanded = sample_distrubtion(probs)

    return recomanded




# x = [reccomand(text) for i in range(1000)]