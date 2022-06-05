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
from class_demo import Demo
from class_demo import Race


print("どこの競馬場？")
name = input()
print("芝orダ？")
log_ground = input()
print("距離？")
log_meter= input()
print("トピックス")
url_topic = input()
print("トピックスは何年分？(最大12年まで)")
cntTopic = int(input())
print("何頭？？　(最大12頭まで)")
hourse_num = int(input())


# トピックからurlの取得と３着以内に入った　馬の前走レースの情報を取得
race = Race(url_topic)
race.getURLTopic()

#入力された年分だけにする
for exp in range(0,cntTopic,1):
    race.createBuyRank(race.get_topic()[exp])
race.setBuyRank(len(race.get_topic()))

demo = Demo(name,log_ground,log_meter)
for i in range(1,hourse_num+1,1):
    demo.createDemo(i)
demo.createExpect(race)


with pd.ExcelWriter("../race_demo/"+ name + log_ground + log_meter +".xlsx") as writer:
    demo.dataBuy.to_excel(writer, sheet_name='sheet1')
    race.dataOdds.to_excel(writer, sheet_name='sheet2')
    demo.dataExpect.to_excel(writer, sheet_name='sheet3')
    


urls = race.get_topic()
for i in range(0,20,1):
    race.getPopSum(urls[i])
    
# 点数のタプル
points = (race.popData1,race.popData2,race.popData3,race.popData4)

# 箱ひげ図
fig, ax = plt.subplots()

bp = ax.boxplot(points)
ax.set_xticklabels(['one', 'two','three','wide'])

plt.title('Box plot')
plt.xlabel('kinds')
plt.ylabel('point')
# Y軸のメモリのrange
plt.ylim([0,30])
plt.yticks([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
plt.grid()

# 描画
plt.show()
fig.savefig("../race_demoImg/"+ name + log_ground + log_meter +".png")