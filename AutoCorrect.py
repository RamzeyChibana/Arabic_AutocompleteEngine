import pandas as pd 
import numpy as np 
import os 
from sklearn.metrics import accuracy_score,f1_score
from tqdm import tqdm
import time

corpus = "Corpus.csv"
corpus2 = "Corpus2.csv"
corpus3 = "Corpus3.csv"
# corpus4 = "Corpus4.csv"


class Corpus:
    def __init__(self,dataframe:pd.DataFrame,seq) -> None:
        self.dataframe = dataframe 
        self.seq = seq
        self.dataframe.set_index(dataframe.keys()[0], inplace=True, drop=False)
        

class AutoCorrect():
    def __init__(self,name = "Untitled",max_corps=4):
        self.name = name 
        self.corps = []
        self.max_corps = max_corps
    def load_corpus(self,corpus_path,seq=1):
        
        if len(self.corps) < self.max_corps : 
            self.corps.append(Corpus(pd.read_csv(corpus_path),seq=seq))
            max_shape = 0
            self.corps = sorted(self.corps,key=lambda x:x.seq,reverse=True)
        else :
            print("To Much Corpuses..")
    
    def get_values(self,result,touken=True):
        allx = []
        new_values = []
        result = result.dropna()
        for x in result[1:]:
            
            if x is not np.nan:
                value ,freq= x.replace(" ","").split("|")
                
                new_values.append([int(freq),value])
        return new_values

    def get_probibilties(self,possiblities:list[str],threshold=0.1):
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
            if len(possiblities) == 0 :
                return new_possiblities 
            return self.get_probibilties(possiblities,threshold=threshold)

    def sample_distrubtion(self,probs):
        probilities , values = zip(*probs)

        ran_value = np.random.choice(values,p=probilities)

        return ran_value
    def best_distrubtion(self,probs):
        probilities , values = zip(*probs)
        i = np.argmax(probilities)
        

        return values[i]
    def random_distrubtion(self,probs):
        probilities , values = zip(*probs)

        ran_value = np.random.choice(values[:3])

        return ran_value

    def get_result(self,corpus,text:str):
        words = text.split()[-corpus.seq:]
        word = " ".join(words)
        
        # Directly access the row by index
        try:
            result = corpus.dataframe.loc[word].squeeze()
        except KeyError:
            result = None  # or handle as appropriate
        
        return result
    
    def recommand(self,text,thershold=0.4):

        for cor in self.corps :
            result = self.get_result(cor,text)

            if result is not None:
                break
        if result is None :
            return "nothing"
        

        result = self.get_values(result)
        if len(result)==0:
            return "nothing"
        probs = self.get_probibilties(result,threshold=thershold)
        recomanded = self.best_distrubtion(probs)

        return recomanded

    def evaluate(self,file):
        with open(file,"r",encoding="utf-8") as file :
            texts = file.read().splitlines()
        self.sliding_window(texts[-250:])


    def sliding_window(self,texts:list[str]):
        preds = []
        targets = []
        
        
        pbar = tqdm(total=len(texts))
        pbar.set_description("Evaluating")
        for text in texts :
            words = text.split()
            words = np.array(words)
            test = ""
            for i,word in enumerate(words[:-1]):
                test +=word 
                pred = self.recommand(test)
                test+=" "
                preds.append(pred)
                targets.append(words[i+1])
            
            pbar.update(1)
        pbar.close()

        print(accuracy_score(targets,preds))
cor = AutoCorrect()

cor.load_corpus(corpus)
cor.load_corpus(corpus2,2)
cor.load_corpus(corpus3,3)
# cor.load_corpus(corpus4,4)


recomanded = cor.recommand("فاز اللاعب")
# print(recomanded)
cor.evaluate("testing.txt")



# x = [reccomand(text) for i in range(1000)]