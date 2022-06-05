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
from class_exp import Exp
print("どこの競馬場？")
name = input()
print("芝orダ？")
log_ground = input()
print("距離？")
log_meter= input()
print("何回回す？？")
loopCnt = int(input())
exp_log = []
print("a=? 0 or 1 or 2")
exp_log.append(1)
print("b=? 0 or 1 or 2")
exp_log.append(1)
print("c=? 0 or 1 or 2")
exp_log.append(1)
print("d=? 0 or 1 or 2")
exp_log.append(1)
print("e=? 0 or 1 or 2")
exp_log.append(1)
print("f=? 0 or 1 or 2")
exp_log.append(1)
print("g=? 0 or 1 or 2")
exp_log.append(1)
print("h=? 0 or 1 or 2")
exp_log.append(1)
print("k=? 0 or 1 or 2")
exp_log.append(1)



main = Exp(name,log_ground,log_meter)
main.create_exp(loopCnt,exp_log)  
main.getMaxInfo()
if(main.data_max["max"][0] < main.getMaxInfo()):
    print("更新")
    main.data_max.loc[0,"max"] = main.getMaxInfo()
    

#次回の指数を調整
# 今は使わない
#     loopExp = ["a","b","c","d","e","f","g","h","k"]
#     loopNum = [0,1,2,3,4,5,6,7,8]
#     for i, j in zip(loopExp,loopNum):
#         main.expChecker(i,j)
    
    with pd.ExcelWriter("../race_exp_result/"+ name + log_ground + log_meter +".xlsx") as writer:
        main.data_exp.to_excel(writer, sheet_name='sheet1')
    
    with pd.ExcelWriter("../maxinfo/"+ name + log_ground + log_meter +".xlsx") as writer:
        main.data_max.to_excel(writer, sheet_name='sheet1')
        main.infoExp.to_excel(writer, sheet_name='sheet2')
        
else:
    print("更新なし")

print(main.getMaxInfo())

