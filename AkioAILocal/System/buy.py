
class Buy:
    def __init__(self,file_name):
        self.df_order = pd.read_excel("../result/" + file_name + ".xlsx","最終結果")
        
        self.dataBuy = pd.DataFrame([ [0]],
                    columns = ["総和"],
                    index = [1,2,3,4,5,6,7,8])
        
    def createBuy2(self,bottom,top,rank):
        
        seq = self.df_order["人気"][0:rank]
        datas = list(itertools.combinations(seq,2))
        for i in range(0,len(datas),1):
            popSum = 0
            for j in range(0,2,1):
                popSum = popSum + int(datas[i][j])
                
                self.dataBuy.loc[i,j+1] = self.vlookup(datas[i][j])
            
            if(popSum >= bottom and popSum <= top):
                self.dataBuy.loc[i,"総和"] = popSum
                
    def createBuy3(self,bottom,top,rank):
        
        seq = self.df_order["人気"][0:rank]
        datas = list(itertools.combinations(seq,3))
        for i in range(0,len(datas),1):
            popSum = 0
            for j in range(0,3,1):
                popSum = popSum + int(datas[i][j])
                
                self.dataBuy.loc[i,j+1] = self.vlookup(datas[i][j])
            
            if(popSum >= bottom and popSum <= top):
                self.dataBuy.loc[i,"総和"] = popSum
                
    
            
    def vlookup(self,value):
        for i in range(0,len(self.df_order),1):
            if(self.df_order["人気"][i] == value):
                name = self.df_order["馬番"][i]
                break
        return name



import pandas as pd
import itertools
print("大会名")
name = input()
print("rank")
rank = int(input())

buy2 = Buy(name)
print("馬連:bottom")
bottom = int(input())
print("馬連:top")
top = int(input())
buy2.createBuy2(bottom,top,rank)

buy3 = Buy(name)
print("３連複:bottom")
bottom = int(input())
print("３連複:top")
top = int(input())
buy3.createBuy3(bottom,top,rank)

with pd.ExcelWriter("../race_demoBuy/"+ name +".xlsx") as writer:
    buy2.dataBuy.sort_values('総和', ascending=False).to_excel(writer, sheet_name='馬連買い目')
    buy3.dataBuy.sort_values('総和', ascending=False).to_excel(writer, sheet_name='3連複買い目')
