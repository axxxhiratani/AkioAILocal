import pandas as pd
import random
import requests
from tqdm import tqdm as tqdm
import statsmodels.api as sm
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score

# 20年分のデータの傾向を分析するクラス
class Tend:
    def __init__(self,file_name):
        self.df_order = pd.read_excel("../race_data/"+file_name + ".xlsx","sheet1")
        
    #データの正規化
        X_name = ["a","b","c","d","e","f","g","h","k"]
        x = self.df_order[X_name]
        stdsc = StandardScaler()
        self.regular_data = stdsc.fit_transform(x)
        
    #保存用のデータを用意
        self.output_data = pd.DataFrame({
                        'result':[],         
                                }) 
        self.tend_data = pd.DataFrame({
                        'a':[], 
                        'b':[], 
                        'c':[], 
                        'd':[], 
                        'e':[], 
                        'f':[], 
                        'g':[], 
                        'h':[], 
                        'k':[], 
                                }) 
        
        self.index_data = pd.DataFrame({
                        'a':[], 
                        'b':[], 
                        'c':[], 
                        'd':[], 
                        'e':[], 
                        'f':[], 
                        'g':[], 
                        'h':[], 
                        'k':[], 
                                }) 
    
    
#race_dataから加工        
    def createData(self):
        for i in range(0,len(self.regular_data),1):
            
            if(self.df_order["target"][i] == 1):
                self.output_data.loc[i,"result"] = 1
            else:
                self.output_data.loc[i,"result"] = 0
            
            
            for j in range(0,len(self.regular_data[i]),1):
                self.output_data.loc[i,j] = (self.regular_data[i][j])
                
                
#kaiki.batで参考にするテーブルを作成する    
    def createTend(self):
        for i in range(0,len(self.output_data),1):
            
            if(self.output_data["result"][i] == 1):
                self.tend_data.loc[i,"a"] = self.output_data[0][i]
                self.tend_data.loc[i,"b"] = self.output_data[1][i]
                self.tend_data.loc[i,"c"] = self.output_data[2][i]
                self.tend_data.loc[i,"d"] = self.output_data[3][i]
                self.tend_data.loc[i,"e"] = self.output_data[4][i]
                self.tend_data.loc[i,"f"] = self.output_data[5][i]
                self.tend_data.loc[i,"g"] = self.output_data[6][i]
                self.tend_data.loc[i,"h"] = self.output_data[7][i]
                self.tend_data.loc[i,"k"] = self.output_data[8][i]
                
                
        self.index_data.loc["avg","a"] = self.tend_data["a"].mean()
        self.index_data.loc["avg","b"] = self.tend_data["b"].mean()
        self.index_data.loc["avg","c"] = self.tend_data["c"].mean()
        self.index_data.loc["avg","d"] = self.tend_data["d"].mean()
        self.index_data.loc["avg","e"] = self.tend_data["e"].mean()
        self.index_data.loc["avg","f"] = self.tend_data["f"].mean()
        self.index_data.loc["avg","g"] = self.tend_data["g"].mean()
        self.index_data.loc["avg","h"] = self.tend_data["h"].mean()
        self.index_data.loc["avg","k"] = self.tend_data["k"].mean()
        

# AIの結果を分析する
class Result:
    def __init__(self,file_name):
        self.df_order = pd.read_excel("../result/"+file_name + ".xlsx","最終結果")
        
        
    #データの正規化
        X_name = ["人気","枠値","斤量値","距離適正","騎手（このレース）","上り","馬実績","馬血統","前走","タイム"]

        x = self.df_order[X_name]
        stdsc = StandardScaler()
        self.regular_data = stdsc.fit_transform(x)
        
    #保存用のデータを用意
        self.output_data = pd.DataFrame({
                        'result':[],         
                                }) 
    

#race_dataから加工        
    def createData(self):
        for i in range(0,len(self.regular_data),1):
            
            if(self.df_order["結果"][i] == 1):
                self.output_data.loc[i,"result"] = 1
            else:
                self.output_data.loc[i,"result"] = 0
            
            
            for j in range(0,len(self.regular_data[i]),1):
                self.output_data.loc[i,j] = (self.regular_data[i][j])