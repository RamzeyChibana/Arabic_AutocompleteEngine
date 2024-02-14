import pandas as pd 
import numpy as np 





class AutoCorrect():
    def __init__(self,corpus_dir) -> None:
        self.dir_corpus = corpus_dir
        self.corpus = self.load_Corpus()

    def load_Corpus(self):
        corpus = pd.read_csv(self.dir_corpus,encoding="UTf-8")
        return corpus

    def recommand(self,text):
        











