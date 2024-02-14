import numpy as np 
import pandas as pd 
import spacy as sp 
from spacy.lang.ar import stop_words
from collections import Counter,defaultdict
import os 
import re




class Corpus():
    def __init__(self,data_path,):
        self.data_path = data_path
        self.files = os.listdir(self.data_path)

    def _get_matches(self,text):
        regular_expertion = r"\(.*?\)|[0-9|\-]+"
        try :
            regex = re.compile(regular_expertion)
            matches = regex.findall(text)
            return matches
        except:
            return None

    def _replace_matches(self,text):
            matches = self._get_matches(text)
            if matches is None :
                return text
            for match in matches :
                text = text.replace(match,"[توكن]",1)
            return text

    def _cleaning(self,text:str):
        stop = ["»","«","#","&","*",".",",","،",":"]
        for char in stop:
            text = text.replace(char,"")
        return text 

    def get_Data(self):
        texts = []
        for file in self.files :
            with open(os.path.join(self.data_path,file),encoding="UTf-8") as file :
                text = file.read()
                texts.append(self._cleaning(self._replace_matches(text)))
        return texts


    def get_frequency_win(self,data:list[str],win=1):

        words = dict()
        for indice,text in enumerate(data[:]) :
            if indice % 1000 == 0 :
                print(f"Processed :{indice}")
            
            text = text.split(" ")
            for idx in range(win,len(text)-1):
                interval = " ".join(text[idx-win:idx])
            
                if interval in words.keys() :
                    words[interval].append(text[idx])
                else :
                    words[interval] = [text[idx],]

    
        for key in words.keys():
            value = dict(Counter(words[key]))
            words[key] = sorted(value.items(),key=lambda item : item[1],reverse=True)

        return words
    
    def get_best_frequency(self,words:dict,best=10):
 

        data = defaultdict(list)
        for key in words.keys() :
        
            data["name"].append(key) 
            for i in range(best) :
                try :
                    data[str(i)].append(str(words[key][i][0])+"|"+str(words[key][i][1]))
                except :
                    data[str(i)].append(None)

        df = pd.DataFrame(data)

        return df


    
    def get_corpus(self,win=1,best=10):
        data = self.get_Data()
        words = self.get_frequency_win(data,win=win)
        corpus = self.get_best_frequency(words,best=best)

        return corpus
    
    def save_corpus(self,dir,corpus:pd.DataFrame):
        
        try :
            corpus.to_csv(dir,encoding="Utf-8",index=False)
            print("..saved Succefuly")
        except :
            print("..Failed to Save")


datapath =  "D:\\df\\ai\\arabic_articls\\Sports"
engein = Corpus(data_path=datapath)

corpus = engein.get_corpus()
engein.save_corpus(corpus=corpus,dir="Corpus.csv")







