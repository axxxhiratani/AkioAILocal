import pandas as pd 
import requests
from bs4 import BeautifulSoup 
import re
from tqdm import tqdm as tqdm
from class_main import Race
from class_main import Tend
from class_main import Exp

print("競馬場")    
log_place = input()
print("コード入力 大井:44 名古屋:48")
log_cord = int(input())
print("芝 or ダ")
log_ground = input()
print("距離")
log_meter = input()
print("内or外:2 or 4")
src = int(input())  
print("右左")
road = input()
print("月")
month = input()
# topicからレースurlを取得
race = Race(log_place,log_cord ,log_ground,log_meter,src,road,month)
race.get_url()
decadeURL = race.get_link()

#十年分を集計
decadeTend = Tend()
decadeTend.create_tend(decadeURL)

decadeTend.fixJockey()
decadeTend.setTime()

#インプット資材作成
main = Exp()
for ageCheck in tqdm(range(0,len(decadeURL),1)):    
    main.create_exp(decadeURL[ageCheck],race,decadeTend)

with pd.ExcelWriter("../race_data/"+str(log_place)+str(log_ground)+str(log_meter)+".xlsx") as writer:
    main.data_exp.to_excel(writer, sheet_name='sheet1')
    

with pd.ExcelWriter("../maxinfo/"+str(log_place)+str(log_ground)+str(log_meter)+".xlsx") as writer:
    race.data_max.to_excel(writer, sheet_name='sheet1')
    race.maxinfoExp.to_excel(writer,sheet_name='sheet2')
    

with pd.ExcelWriter("../race_exp/"+str(log_place)+str(log_ground)+str(log_meter)+".xlsx") as writer:
    decadeTend.data_frame.to_excel(writer, sheet_name='sheet1')
    decadeTend.data_jockey.to_excel(writer, sheet_name='sheet2')
    decadeTend.data_blood.to_excel(writer, sheet_name='sheet3')
    decadeTend.data_prev.to_excel(writer, sheet_name='sheet4')
    decadeTend.data_jockey.to_excel(writer, sheet_name='sheet5')
    decadeTend.timeInfo.to_excel(writer,sheet_name='sheet6')
