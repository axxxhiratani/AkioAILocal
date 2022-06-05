import pandas as pd
import random
import requests
from tqdm import tqdm as tqdm
import statsmodels.api as sm
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
from class_processing import Tend
from class_processing import Result


# 競馬場と距離のデータを加工
print("何処の競馬場？？")
area = input()
print("芝 or ダ？？")
ground = input()
print("距離は？？")
meter = input()

file_name = area + ground + meter

tend_data = Tend(file_name)
tend_data.createData()
tend_data.createTend()
tend_data.output_data.to_csv("../processing_data/"+ file_name +".csv",encoding="shift_jis")
tend_data.index_data.to_csv("../processing_dataTend/"+ file_name +".csv",encoding="shift_jis")

# 結果のデータを加工
print("resultのファイル名を入力してください")
print("終了するなら:Enter")

result_file_name = input()

game_data = Result(result_file_name)
game_data.createData()
game_data.output_data.to_csv("../processing_data/"+ result_file_name +".csv",encoding="shift_jis")