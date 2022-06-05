import pandas as pd
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
from class_output import Output
from class_output import Horse
from class_output import Tend

print("どこの競馬場？")
name = input()
print("芝orダ？")
log_ground = input()
print("距離？")
log_meter= input()
print("大会名は？")
output_name = input()
print("urlを入力してください。(出馬表)")
url = input()

tend = Tend(name,log_ground,log_meter)
main = Output(url)
main.createOutput(tend)
main.createTable2()
main2 = Output(url)
main2.createOutput(tend)
tend.changeTend()
word = pd.read_html(url,header = 1)[0]
word.drop(["枠","性齢","馬体重(増減)","印","厩舎","登録","メモ","斤量","騎手"],axis = 1,inplace = True)
word["ランク"] = 0
for i in range(0,len(main.result),1):
    word["ランク"][i] = main2.result["斤量値"][i] + main2.result["前走"][i] + main2.result["馬実績"][i] + main2.result["馬血統"][i] + main2.result["上り"][i] 
words = pd.read_html(url,header = 1)[0]
words.drop(["枠","性齢","馬体重(増減)","印","厩舎","登録","メモ","斤量","馬名"],axis = 1,inplace = True)
words["ランク"] = 0
for i in range(0,len(main.result),1):
    words["ランク"][i] = str(main2.result["騎手（このレース）"][i])[0:5]+"%"
with pd.ExcelWriter("../result/"+output_name+'.xlsx') as writer:
    tend.df_order.to_excel(writer, sheet_name='傾向')
    word.to_excel(writer, sheet_name='競走馬')
    words.to_excel(writer, sheet_name='騎手')
    main.result.sort_values('指数', ascending=False).to_excel(writer, sheet_name='最終結果')
    




