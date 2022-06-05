import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from tqdm import tqdm as tqdm
import statistics
import numpy as np
import math
import statsmodels.api as sm
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt

class Demo:
    def __init__(self,name,log_ground,log_meter):
        file_name = name + log_ground + log_meter
        self.result = pd.read_excel("../race_data/" + file_name + ".xlsx","sheet1")
        self.data_exp = pd.read_excel("../race_exp_result/" + file_name + ".xlsx","sheet1")
        
        self.dataBuy = pd.DataFrame([ [0,0,0,0,0]],
                    columns = ["単","連","複","ワイド","複勝"],
                    index = [1,2,3,4,5,6,7,8,9,10,11,12])
        
        self.dataExpect = pd.DataFrame([ [0,0,0,0]],
                    columns = ["馬連","馬単","三連複","三連単"],
                    index = [1,2,3,4,5,6,7,8,9,10,11,12])
        
        
        
        X_name = ["a","b","c","d","e","f","g","h","k"]
        x = self.result[X_name]
        stdsc = StandardScaler()
        self.X = stdsc.fit_transform(x)
        
        
        self.cntA = 0
        self.cntB = 0
        self.cntC = 0
        self.cntD = 0
         
        
    def createExpect(self,race):
        
        self.dataExpect.loc[1,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][1]) - 0
        self.dataExpect.loc[2,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][2]) - 100 
        self.dataExpect.loc[3,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][3]) - 300
        self.dataExpect.loc[4,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][4]) - 600
        self.dataExpect.loc[5,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][5]) - 1000
        self.dataExpect.loc[6,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][6]) - 1500
        self.dataExpect.loc[7,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][7]) - 2100
        self.dataExpect.loc[8,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][8]) - 2800
        self.dataExpect.loc[9,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][9]) - 3600
        self.dataExpect.loc[10,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][10]) - 4500
        self.dataExpect.loc[11,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][11]) - 5500
        self.dataExpect.loc[12,"馬連"] = (race.dataOdds["オッズ"]["馬連"])*(self.dataBuy["連"][12]) - 6600


        
        self.dataExpect.loc[1,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][1]) - 0
        self.dataExpect.loc[2,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][2]) - 200
        self.dataExpect.loc[3,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][3]) - 600
        self.dataExpect.loc[4,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][4]) - 1200
        self.dataExpect.loc[5,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][5]) - 2000
        self.dataExpect.loc[6,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][6]) - 3000
        self.dataExpect.loc[7,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][7]) - 4200
        self.dataExpect.loc[8,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][8]) - 5600
        self.dataExpect.loc[9,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][9]) - 7200
        self.dataExpect.loc[10,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][10]) - 9000
        self.dataExpect.loc[11,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][11]) - 11000
        self.dataExpect.loc[12,"馬単"] = (race.dataOdds["オッズ"]["馬単"])*(self.dataBuy["連"][12]) - 13200

        
        self.dataExpect.loc[1,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][1]) - 0
        self.dataExpect.loc[2,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][2]) - 0
        self.dataExpect.loc[3,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][3]) - 100
        self.dataExpect.loc[4,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][4]) - 400
        self.dataExpect.loc[5,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][5]) - 1000
        self.dataExpect.loc[6,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][6]) - 2000
        self.dataExpect.loc[7,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][7]) - 3500
        self.dataExpect.loc[8,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][8]) - 5600
        self.dataExpect.loc[9,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][9]) - 8400
        self.dataExpect.loc[10,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][10]) - 12000
        self.dataExpect.loc[11,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][11]) - 16500
        self.dataExpect.loc[12,"三連複"] = (race.dataOdds["オッズ"]["三連複"])*(self.dataBuy["複"][12]) - 22000
        


        self.dataExpect.loc[1,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][1]) - 0
        self.dataExpect.loc[2,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][2]) - 0
        self.dataExpect.loc[3,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][3]) - 600
        self.dataExpect.loc[4,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][4]) - 2400
        self.dataExpect.loc[5,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][5]) - 6000
        self.dataExpect.loc[6,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][6]) - 12000
        self.dataExpect.loc[7,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][7]) - 21000
        self.dataExpect.loc[8,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][8]) - 33600
        self.dataExpect.loc[9,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][9]) - 54000
        self.dataExpect.loc[10,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][10]) - 72000
        self.dataExpect.loc[11,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][11]) - 99000
        self.dataExpect.loc[12,"三連単"] = (race.dataOdds["オッズ"]["三連単"])*(self.dataBuy["複"][12]) - 132000





            
    def createDemo(self,rankBuy):
        
        self.result["sum"] = 0
        self.result["akioRank"] = 0
        self.result["difference"] = 0
        

        
        a = self.data_exp["a"].mean()
        b = self.data_exp["b"].mean()
        c = self.data_exp["c"].mean()
        d = self.data_exp["d"].mean()
        e = self.data_exp["e"].mean()
        f = self.data_exp["f"].mean()
        g = self.data_exp["g"].mean()
        h = self.data_exp["h"].mean()
        k = self.data_exp["k"].mean()
        
        
        




        for i in (range(0,len(self.result),1)):
            
            
            self.result.loc[i,"sum"] =  (self.X[i][0] * a) + (self.X[i][1] * b) + (self.X[i][2] * c) + (self.X[i][3] * d) + (self.X[i][4] * e) + (self.X[i][5] * f) + (self.X[i][6] * g) + (self.X[i][7] * h) + (self.X[i][8] * k)  
            
            
            
        for i in range(0,len(self.result),1):
            
            if( self.result["target"][i] == 1):
                start = self.result["start"][i]
                length = self.result["length"][i]
            self.result.loc[i,"akioRank"] = (self.result["sum"][start:start+length].rank(ascending=False)[i])
            self.result.loc[i,"difference"] = self.result["target"][i] - self.result.loc[i,"akioRank"]

        
        index = -1
        rankCnt = 0
        for i in range(0,len(self.result),1):
            if( self.result["start"][i] > index):
                
                
                #上位index頭が単勝的中できるかどうか
                if(self.result["akioRank"][i] <= rankBuy):
                    self.dataBuy["単"][rankBuy] = self.dataBuy["単"][rankBuy] + 1
                
                
                #上位index頭が馬連的中できるかどうか
                if(self.result["akioRank"][i] <= rankBuy and self.result["akioRank"][i+1] <= rankBuy):
                    self.dataBuy["連"][rankBuy] = self.dataBuy["連"][rankBuy] + 1
                
                #上位index頭が３連複的中できるかどうか
                if(self.result["akioRank"][i] <= rankBuy and self.result["akioRank"][i+1] <= rankBuy and self.result["akioRank"][i+2] <= rankBuy):
                    self.dataBuy["複"][rankBuy] = self.dataBuy["複"][rankBuy] + 1
                
                #上位index頭がワイド的中できるかどうか
                if(self.result["akioRank"][i] <= rankBuy):
                    if( self.result["akioRank"][i+1] <= rankBuy or self.result["akioRank"][i+2] <= rankBuy):
                        self.dataBuy["ワイド"][rankBuy] = self.dataBuy["ワイド"][rankBuy] + 1
                else:
                    if( self.result["akioRank"][i+1] <= rankBuy and self.result["akioRank"][i+2] <= rankBuy):
                        self.dataBuy["ワイド"][rankBuy] = self.dataBuy["ワイド"][rankBuy] + 1

                #上位index頭が複勝的中できるかどうか
                if(self.result["akioRank"][i] <= rankBuy or self.result["akioRank"][i + 1] <= rankBuy or self.result["akioRank"][i + 2] <= rankBuy):
                    self.dataBuy["複勝"][rankBuy] = self.dataBuy["複勝"][rankBuy] + 1

                
                    
                
                index = index + self.result["length"][i]
                rankCnt = rankCnt + 1    
        
        self.dataBuy.loc[rankBuy,"単"] = self.dataBuy["単"][rankBuy] / rankCnt
        self.dataBuy.loc[rankBuy,"連"] = self.dataBuy["連"][rankBuy] / rankCnt
        self.dataBuy.loc[rankBuy,"複"] = self.dataBuy["複"][rankBuy] / rankCnt
        self.dataBuy.loc[rankBuy,"ワイド"] = self.dataBuy["ワイド"][rankBuy] / rankCnt
        self.dataBuy.loc[rankBuy,"複勝"] = self.dataBuy["複勝"][rankBuy] / rankCnt
        
class Race:
    def __init__(self,url_topic):
        
        self.url_topic = url_topic
        self.A = 0
        self.B = 0
        self.C = 0
        self.D = 0
        self.cntA = 0
        self.cntB = 0
        self.cntC = 0
        self.cntD = 0
        self.dataOdds = pd.DataFrame([ [0]],
                    columns = ["オッズ"],
                    index = ["馬連","馬単","三連複","三連単"])
        
        self.popData1 = []
        self.popData2 = []
        self.popData3 = []
        self.popData4 = []
        
        
    #トピックのurlを返す
    def get_topic(self):
        return self.race_id_list 
        
        
        
    #平均配当を計算rac
    def createBuyRank(self,exp):
        response = requests.get(exp)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.findAll("table",class_="pay_table_01")
        cntOddsValue = 0
        for tb in table:
            for td in tb.findAll("td",class_="txt_r"):

                if(cntOddsValue ==6):
                    if(int(td.text.replace(",","")) <= 50000):
                        self.A = self.A + int(td.text.replace(",",""))
                    else:
                        self.A = self.A + 50000
                    self.cntA = self.cntA + 1



                if(cntOddsValue ==10):
                    if(int(td.text.replace(",","")) <= 100000):
                        self.B = self.B + int(td.text.replace(",",""))
                    else:
                        self.B = self.B + 100000
                    self.cntB = self.cntB + 1


                if(cntOddsValue ==12):
                    if(int(td.text.replace(",","")) <= 150000):
                        self.C = self.C + int(td.text.replace(",",""))
                    else:
                        self.C = self.C + 150000
                    self.cntC = self.cntC + 1

                if(cntOddsValue ==14):
                    if(int(td.text.replace(",","")) <= 300000):
                        self.D = self.D + int(td.text.replace(",",""))
                    else:
                        self.D = self.D + 300000
                    self.cntD = self.cntD + 1
                cntOddsValue = cntOddsValue + 1
                
    #平均配当をセット
    def setBuyRank(self,size):
        self.dataOdds.loc["馬連","オッズ"] = self.A / self.cntA
        self.dataOdds.loc["馬単","オッズ"] = self.B / self.cntB
        self.dataOdds.loc["三連複","オッズ"] = self.C / self.cntC
        self.dataOdds.loc["三連単","オッズ"] = self.D / self.cntD

        
        
        
        
    
    def getURLTopic(self):
        #トピックのurl取得
        
        try:
            response = requests.get(self.url_topic)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table',class_="All_Special_Table")
            self.race_id_list = [] 
            for tr in table.findAll("tr"):
                trs = tr.findAll("td",class_="race_name Txt_Bold Txt_L")
                cnt = 0
                for each in trs:
                    try:
                        link = each.find('a')['href']
                        self.race_id_list.append(link)
                        cnt = cnt + 1
                    except:
                        pass  
        
        except:
            
            #urlゲット
            response = requests.get(self.url_topic)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table',class_="nk_tb_common race_table_01")
            self.race_id_list = [] 
            for tr in table.findAll("tr"):
                trs = tr.findAll("td",class_="txt_l")
                cnt = 0
                for each in trs:
                    try:
                        if(cnt % 6 ==0):
                            link = each.find('a')['href']
                            self.race_id_list.append("https://db.netkeiba.com" + link)
                        cnt = cnt + 1
                    except:
                        pass
                    
    def getPopSum(self,url):
        
        popSum1 = 0
        popSum2 = 0
        popSum3 = 0
        popSum4 = 0
        popSum5 = 0
        popSum6 = 0
        
        data = pd.read_html(url,header=0)[0]
        for x,y in zip(data['着順'],data['人気']):
            
            try:
                if(int(x) <= 1):
                    popSum1 = popSum1 + int(y)
                    popSum4 = popSum4 + int(y)
                    popSum5 = popSum5 + int(y)

                if(int(x) <= 2):
                    popSum2 = popSum2 + int(y)
                    popSum4 = popSum4 + int(y)
                    popSum6 = popSum6 + int(y)

                if(int(x) <= 3):
                    popSum3 = popSum3 + int(y)
                    popSum5 = popSum5 + int(y)
                    popSum6 = popSum6 + int(y)
            except:
                continue
                
        self.popData1.append(popSum1)
        self.popData2.append(popSum2)
        self.popData3.append(popSum3)
        self.popData4.append(popSum4)
        self.popData4.append(popSum5)
        self.popData4.append(popSum6)