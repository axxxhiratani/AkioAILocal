import pandas as pd
import itertools
from class_buy import Buy

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

print("rank")
rank = int(input())
buy3 = Buy(name)
print("３連複:bottom")
bottom = int(input())
print("３連複:top")
top = int(input())
buy3.createBuy3(bottom,top,rank)

with pd.ExcelWriter("../race_demoBuy/"+ name +".xlsx") as writer:
    buy2.dataBuy.sort_values('総和', ascending=False).to_excel(writer, sheet_name='馬連買い目')
    buy3.dataBuy.sort_values('総和', ascending=False).to_excel(writer, sheet_name='3連複買い目')
