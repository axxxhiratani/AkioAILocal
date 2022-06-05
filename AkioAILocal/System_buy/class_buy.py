import pandas as pd
import itertools

class Buy:
    def __init__(self,file_name):
        self.df_order = pd.read_excel("../result/" + file_name + ".xlsx","最終結果")
        
        self.dataBuy = pd.DataFrame([ [0]],
                    columns = ["総和"],
                    index = [])
        

        #指数上位rank頭から馬連ボックスを全通り抽出
        # 2頭の人気の総和がbottom以上、top以下は除く
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
        

        #指数上位rank頭から3連複を全通り抽出
        # 3頭の人気の総和がbottom以上、top以下は除く
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


