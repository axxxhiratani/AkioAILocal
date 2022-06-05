import pandas as pd
import random
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm as tqdm
import statsmodels.api as sm
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
class Exp:
    def __init__(self,name,log_ground,log_meter):
        self.data_exp = pd.DataFrame({
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
        
        
        file_name = name + log_ground + log_meter
        self.df_order = pd.read_excel("../race_data/" + file_name + ".xlsx","sheet1")
        
        self.data_max = pd.read_excel("../maxinfo/" + file_name + ".xlsx","sheet1")
        
        self.infoExp = pd.read_excel("../maxinfo/" + file_name + ".xlsx","sheet2")
        
        
        X_name = ["a","b","c","d","e","f","g","h","k"]
        x = self.df_order[X_name]
        stdsc = StandardScaler()
        self.X = stdsc.fit_transform(x)
        
        self.expCnt = 0
        self.rankMax = 0
        self.loopCnt = 0
        
        
    def getMaxInfo(self):
        return self.rankMax
        
        
        
    def create_exp(self,loopCnt,exp_log):
                
        self.df_order["sum"] = 0
        self.df_order["rank"] = 0
        
        for zzz in tqdm(range(0,loopCnt,1)):

            #指数aのセット
            if(exp_log[0] == 0):
                a = 0
            elif(exp_log[0] == 2):
                a = 1
            else :
                a = random.uniform(1,0)
            
            #指数bのセット
            if(exp_log[1] == 0):
                b = 0
            elif(exp_log[1] == 2):
                b = 1
            else :
                b = random.uniform(1,0)
                
            #指数cのセット
            if(exp_log[2] == 0):
                c = 0
            elif(exp_log[2] == 2):
                c = 1
            else :
                c = random.uniform(1,0)
                
            #指数dのセット
            if(exp_log[3] == 0):
                d = 0
            elif(exp_log[3] == 2):
                d = 1
            else :
                d = random.uniform(1,0)
                
            #指数eのセット
            if(exp_log[4] == 0):
                e = 0
            elif(exp_log[4] == 2):
                e = 1
            else :
                e = random.uniform(1,0)
                
            #指数fのセット
            if(exp_log[5] == 0):
                f = 0
            elif(exp_log[5] == 2):
                f = 1
            else :
                f = random.uniform(1,0)
                
            #指数gのセット
            if(exp_log[6] == 0):
                g = 0
            elif(exp_log[6] == 2):
                g = 1
            else :
                g = random.uniform(1,0)
                
            #指数hのセット
            if(exp_log[7] == 0):
                h = 0
            elif(exp_log[7] == 2):
                h = 1
            else :
                h = random.uniform(1,0)
                
            #指数kのセット
            if(exp_log[8] == 0):
                k = 0
            elif(exp_log[8] == 2):
                k = 1
            else :
                k = random.uniform(1,0)
            
                    
            for i in range(0,len(self.df_order),1):

                self.df_order.loc[i,"sum"] =  (self.X[i][0]*a)+(self.X[i][1]*b)+(self.X[i][2]*c)+(self.X[i][3]*d)+(self.X[i][4]*e)+(self.X[i][5]*f)+(self.X[i][6]*g)+(self.X[i][7]*h)+(self.X[i][8]*k)

            for i in range(0,len(self.df_order),1):

                if( self.df_order["target"][i] == 1):
                    start = self.df_order["start"][i]
                    length = self.df_order["length"][i]
                
                self.df_order.loc[i,"rank"] = (self.df_order["sum"][start:start+length].rank(ascending=False)[i])


    
            if(self.df_order.corr().loc["rank","target"] > self.rankMax):
                self.rankMax = self.df_order.corr().loc["rank","target"]
                self.expCnt = 0
                self.data_exp.loc[self.expCnt,:] = [a,b,c,d,e,f,g,h,k]

    #指数調整
    #indexは0~7
    #rowはa~b
    #今は使用しない
    def expChecker(self,row,index):
        
        if(self.data_exp[row][0] > 0.8):
            self.infoExp.loc[index,"max"] = 1
            self.infoExp.loc[index,"min"] = 1
            
        elif(self.data_exp[row][0] < 0.1):
            self.infoExp.loc[index,"max"] = 0
            self.infoExp.loc[index,"min"] = 0
            