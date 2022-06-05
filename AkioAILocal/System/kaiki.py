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
        
        
        self.maxA = self.infoExp["max"][0]
        self.minA = self.infoExp["min"][0]
        self.maxB = self.infoExp["max"][1]
        self.minB = self.infoExp["min"][1]
        self.maxC = self.infoExp["max"][2]
        self.minC = self.infoExp["min"][2]
        self.maxD = self.infoExp["max"][3]
        self.minD = self.infoExp["min"][3]
        self.maxE = self.infoExp["max"][4]
        self.minE = self.infoExp["min"][4]
        self.maxF = self.infoExp["max"][5]
        self.minF = self.infoExp["min"][5]
        self.maxG = self.infoExp["max"][6]
        self.minG = self.infoExp["min"][6]
        self.maxH = self.infoExp["max"][7]
        self.minH = self.infoExp["min"][7]
        self.maxK = self.infoExp["max"][8]
        self.minK = self.infoExp["min"][8]
        
        
        
        
        X_name = ["a","b","c","d","e","f","g","h","k"]
        x = self.df_order[X_name]
        stdsc = StandardScaler()
        self.X = stdsc.fit_transform(x)
        
        self.expCnt = 0
        self.rankMax = 0
        self.loopCnt = 0
        
        
    def getMaxInfo(self):
        return self.rankMax
        
        
        
    def create_exp(self,loopCnt):
                
        self.df_order["sum"] = 0
        self.df_order["rank"] = 0
        
        for zzz in tqdm(range(0,loopCnt,1)):
            
            a = random.uniform(self.maxA, self.minA)
            b = random.uniform(self.maxB, self.minB)
            c = random.uniform(self.maxC, self.minC)
            d = random.uniform(self.maxD, self.minD)
            e = random.uniform(self.maxE, self.minE)
            f = random.uniform(self.maxF, self.minF)
            g = random.uniform(self.maxG, self.minG)
            h = random.uniform(self.maxH, self.minH)
            k = random.uniform(self.maxH, self.minH)

            for i in range(0,len(self.df_order),1):

                self.df_order.loc[i,"sum"] =  (self.X[i][0]*a)+(self.X[i][1]*b)+(self.X[i][2]*c)+(self.X[i][3]*d)+(self.X[i][4]*e)+(self.X[i][5]*f)+(self.X[i][5]*g)+(self.X[i][6]*h)+(self.X[i][7]*k)

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
    def expChecker(self,row,index):
        
        if(self.data_exp[row][0] > 0.65):
            self.infoExp.loc[index,"max"] = 1
            self.infoExp.loc[index,"min"] = 0
            
        elif(self.data_exp[row][0] > 0.85):
            self.infoExp.loc[index,"max"] = 1.5
            self.infoExp.loc[index,"min"] = 0.5
            
        if(self.data_exp[row][0] < -0.1):
            self.infoExp.loc[index,"max"] = 0.5
            self.infoExp.loc[index,"min"] = 0
            
        elif(self.data_exp[row][0] < -0.5):
            self.infoExp.loc[index,"max"] = 0
            self.infoExp.loc[index,"max"] = 0

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
print("どこの競馬場？")
name = input()
print("芝orダ？")
log_ground = input()
print("距離？")
log_meter= input()
print("何回回す？？")
loopCnt = int(input())

main = Exp(name,log_ground,log_meter)
main.create_exp(loopCnt)  
main.getMaxInfo()
if(main.data_max["max"][0] < main.getMaxInfo()):
    print("更新")
    main.data_max.loc[0,"max"] = main.getMaxInfo()
    
    
    loopExp = ["a","b","c","d","e","f","g","h","k"]
    loopNum = [0,1,2,3,4,5,6,7,8]
    
    for i, j in zip(loopExp,loopNum):
        main.expChecker(i,j)
    
    
    
    with pd.ExcelWriter("../race_exp_result/"+ name + log_ground + log_meter +".xlsx") as writer:
        main.data_exp.to_excel(writer, sheet_name='sheet1')
    
    with pd.ExcelWriter("../maxinfo/"+ name + log_ground + log_meter +".xlsx") as writer:
        main.data_max.to_excel(writer, sheet_name='sheet1')
        main.infoExp.to_excel(writer, sheet_name='sheet2')
        
else:
    print("更新なし")

print(main.getMaxInfo())

