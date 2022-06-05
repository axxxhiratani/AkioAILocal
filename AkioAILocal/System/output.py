class Output:
    def __init__(self,url):
        table = pd.read_html(url,header = 1)[0]
        table["性別"] = table["性齢"].map(lambda x: str(x)[0])
        table["年齢"] = table["性齢"].map(lambda x: str(x)[1:]).astype(int)
        table.drop(["性齢","馬体重(増減)","印","厩舎","Unnamed: 9","登録","メモ"],axis = 1,inplace = True)
        self.result =table
        self.url = url
        
        
    def createOutput(self):
        df = pd.read_html(self.url)[0]
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for tr in soup.find_all("tr"):
            trs = tr.find_all("span",class_="HorseName")
            for each in trs:
                try:
                    link = each.find('a')['href']
                    links.append(link)
                except:
                    pass

        df['HorseLink'] = links
        
        
        
        
        
#         horseインスタンス
        horse = Horse()

        for i in range(0,len(df),1):
            try:
                data_pre_race = pd.read_html(df["HorseLink"][i])[3]
                name = df.loc[i]["馬名"][0] 
                horse.data_horse.loc[i,:] = [name,horse.pre_race(1,data_pre_race),horse.pre_race(2,data_pre_race),horse.pre_race(3,data_pre_race),horse.pre_race(4,data_pre_race),horse.pre_race(5,data_pre_race)]
                if(horse.data_horse["前走"][i] == 1 and horse.data_horse["適正"][i] ==1 and horse.data_horse["能力"][i] == 1):
                    data_pre_race = pd.read_html(df["HorseLink"][i])[4]
                    horse.data_horse.loc[i,:] = [name,horse.pre_race(1,data_pre_race),horse.pre_race(2,data_pre_race),horse.pre_race(3,data_pre_race),horse.pre_race(4,data_pre_race),horse.pre_race(5,data_pre_race)]
                    if(horse.data_horse["前走"][i] == 1 and horse.data_horse["適正"][i] ==1 and horse.data_horse["能力"][i] == 1):
                        data_pre_race = pd.read_html(df["HorseLink"][i])[5]
                        horse.data_horse.loc[i,:] = [name,horse.pre_race(1,data_pre_race),horse.pre_race(2,data_pre_race),horse.pre_race(3,data_pre_race),horse.pre_race(4,data_pre_race),horse.pre_race(5,data_pre_race)]
            except:
                horse.data_horse.loc[i,:] = [name,0,0,0,0,0]

                
                


        #血統を保存
        #前走を保存
        blood_1 = []
        blood_2 = []
        prev_game = []
        for x in df['HorseLink']:
            blood = pd.read_html(x)[2]
            blood_1.append(blood[0][0])
            blood_2.append(blood[1][2])
            try:
                game = pd.read_html(x)[3]
                prev_game.append(game["レース名"][0])
            except:
                game = pd.read_html(x)[4]
                prev_game.append(game["レース名"][0])
                
        self.result['blood_1'] = blood_1
        self.result['blood_2'] = blood_2  
        self.result['前走大会'] = prev_game
    
       


        self.result["枠値"] = 0
        self.result["斤量値"] = 0
        self.result["距離適正"] = 0
        self.result["騎手（このレース）"] = 0
        self.result["上り"] = 0
        self.result["馬実績"] = 0
        self.result["馬血統"] = 0
        self.result["前走"] = 0
        self.result["タイム"] = 0
        
        
        
        self.result["ランク"] = 0
        self.result["指数"] = 0
        
        
        a = (tend.data_exp["a"].mean())
        b = (tend.data_exp["b"].mean())
        c = (tend.data_exp["c"].mean())
        d = (tend.data_exp["d"].mean())
        e = (tend.data_exp["e"].mean())
        f = (tend.data_exp["f"].mean())
        g = (tend.data_exp["g"].mean())
        h = (tend.data_exp["h"].mean())
        k = (tend.data_exp["k"].mean())
        
        





        for i in tqdm(range(0,len(self.result),1)):
            self.result.loc[i,"枠値"] =  (float(tend.vlookup(1,self.result["枠"][i])) + tend.vlookup(5,self.result["馬番"][i]) )
            self.result.loc[i,"斤量値"] = int(self.result["斤量"][i])
            self.result.loc[i,"距離適正"] =  horse.vlookup(2,self.result["馬名"][i])
            self.result.loc[i,"騎手（このレース）"] =  (tend.vlookup(4,self.result["騎手"][i].replace(' ', '')) + tend.vlookup(8,self.result["騎手"][i].replace(' ', '')))/2
            self.result.loc[i,"上り"] = horse.vlookup(4,self.result["馬名"][i])
            self.result.loc[i,"馬実績"] = (horse.vlookup(1,self.result["馬名"][i]) + horse.vlookup(3,self.result["馬名"][i])) /2
            self.result.loc[i,"馬血統"] =  (tend.vlookup(6,self.result["blood_1"][i]) + tend.vlookup(6,self.result["blood_2"][i]))
            self.result.loc[i,"前走"] = (tend.vlookup(7,self.result["前走大会"][i]))
            self.result.loc[i,"タイム"] = horse.vlookup(5,self.result["馬名"][i])
                                       
        X_name = ["枠値","斤量値","距離適正","騎手（このレース）","上り","馬実績","馬血統","前走","タイム"]
        x = self.result[X_name]
        stdsc = StandardScaler()
        self.X = stdsc.fit_transform(x)    
                
        
        for i in tqdm(range(0,len(self.result),1)):
            self.result.loc[i,"指数"] =  self.X[i,0]*a + self.X[i,1]*b + self.X[i,2]*c +  self.X[i,3]*d + self.X[i,4]*e + self.X[i,5]*f + self.X[i,6]*g + self.X[i,7]*h + self.X[i,8]*k
              
            
            
            
    
            
    def createTable(self):
        self.result.drop(["枠","斤量","性別","年齢","blood_1","blood_2","前走大会"],axis = 1,inplace = True)
        self.result["指数"] = 0
        
        
#     標準とexpの合成
        for i in range(0,len(self.result),1):
            self.result["指数"][i]= float(main.result["指数"][i])
            
    def createTable2(self):
        self.result.drop(["枠","斤量","性別","年齢","枠値","斤量値","距離適正","騎手（このレース）","上り","馬実績","馬血統","前走","ランク","blood_1","blood_2","前走大会","タイム"],axis = 1,inplace = True)
#         self.result.drop(["枠","斤量","人気","性別","年齢","ランク","blood_1","blood_2","前走大会"],axis = 1,inplace = True)
            



class Horse:
    def __init__(self,):
        self.data_horse = pd.DataFrame({
                                'name':[],
                                '前走':[],
                                '適正':[],
                                '能力':[],
                                '上り':[],
                                'タイム':[],
                                })
        
        
    def pre_race(self,case,data_pre_race):
            point = 1
            point_cnt = 1
        #     前走を評価
            if(case == 1):     

                try: 
                    if(data_pre_race["着順"][1]!="除" and data_pre_race["着順"][1]!="中" and data_pre_race["着順"][1]!="取"):
                        if(data_pre_race["レース名"][0].endswith('(G', 0, len(data_pre_race["レース名"][0])-2)): 
                            point = point + 14
                            if(int(data_pre_race["着順"][0]) <= 8 ):
                                point = point + 15
                                if(int(data_pre_race["着順"][0]) <= 3):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][0]) <= 1):
                                        point = point + 10


                        else:
                            if(int(data_pre_race["着順"][0]) <= 3 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][0]) <= 2):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][0]) <= 1):
                                        point = point + 10

                except:
                    point = point
                    
                    




        #     距離適正を評価       
            if(case == 2):

                try: 
                    for tmp in range(0,len(data_pre_race[0:])-1,1):
                        if(data_pre_race["着順"][tmp]!="除" and data_pre_race["着順"][tmp]!="中" and data_pre_race["着順"][tmp]!="取"):
                            if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2) and data_pre_race["距離"][tmp] == tend.getGround(0)):
                                point_cnt = point_cnt + 1 
                                point = point + 19
                                if(int(data_pre_race["着順"][tmp]) <= 8 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 3):
                                        point = point + 15
                                        
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 25
                                            
                                    


                            elif(data_pre_race["距離"][tmp] == tend.getGround(0)):
                                point_cnt = point_cnt + 1 
                                if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 2):
                                        point = point + 15
                                        
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 25
                                            
                                    
                                                        
                            if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2) and (data_pre_race["距離"][tmp] == tend.getGround(-100) or data_pre_race["距離"][tmp] == tend.getGround(-200) or data_pre_race["距離"][tmp] == tend.getGround(-300) or data_pre_race["距離"][tmp] == tend.getGround(-400))):
                                point_cnt = point_cnt + 1 
                                point = point + 5
                                if(int(data_pre_race["着順"][tmp]) <= 8 ):
                                    point = point + 5
                                    if(int(data_pre_race["着順"][tmp]) <= 3):
                                        point = point + 15
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point+5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 25
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point+15
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 2
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 3
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 4
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 4
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 6


                            elif(data_pre_race["距離"][tmp] == tend.getGround(-100) or data_pre_race["距離"][tmp] == tend.getGround(-200) or data_pre_race["距離"][tmp] == tend.getGround(-300) or data_pre_race["距離"][tmp] == tend.getGround(-400)):
                                point_cnt = point_cnt + 1 
                                if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                    point = point + 5
                                    if(int(data_pre_race["着順"][tmp]) <= 1):
                                        point = point + 10
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point + 5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 15
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point + 15
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 4
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 4
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 6    


                            if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2) and ( data_pre_race["距離"][tmp] == tend.getGround(-500) or data_pre_race["距離"][tmp] == tend.getGround(-600) or data_pre_race["距離"][tmp] == tend.getGround(-700) or data_pre_race["距離"][tmp] == tend.getGround(-800) )):
                                point_cnt = point_cnt + 1 
                                point = point + 5
                                if(int(data_pre_race["着順"][tmp]) <= 8 ):
                                    point = point + 5
                                    if(int(data_pre_race["着順"][tmp]) <= 3):
                                        point = point + 10
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point+10
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 20
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point + 25
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 4
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 4
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 4
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 8
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 8
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 8


                            elif(data_pre_race["距離"][tmp] == tend.getGround(-500) or data_pre_race["距離"][tmp] == tend.getGround(-600) or data_pre_race["距離"][tmp] == tend.getGround(-700) or data_pre_race["距離"][tmp] == tend.getGround(-800)):
                                point_cnt = point_cnt + 1 
                                if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                    point = point + 5
                                    if(int(data_pre_race["着順"][tmp]) <= 1):
                                        point = point + 5
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point + 10
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 10
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point + 20
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 4
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 4
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 4
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 6
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 6
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 6


                            if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2) and ( data_pre_race["距離"][tmp] == tend.getGround(100) or data_pre_race["距離"][tmp] == tend.getGround(200) or data_pre_race["距離"][tmp] == tend.getGround(300) or data_pre_race["距離"][tmp] == tend.getGround(400) ) ):
                                point_cnt = point_cnt + 1 
                                
                                if(int(data_pre_race["着順"][tmp]) <= 5 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 3):
                                        point = point + 20
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point+5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 30
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point+5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 2


                            elif(data_pre_race["距離"][tmp] == tend.getGround(100) or data_pre_race["距離"][tmp] == tend.getGround(200) or data_pre_race["距離"][tmp] == tend.getGround(300) or data_pre_race["距離"][tmp] == tend.getGround(400)):
                                point_cnt = point_cnt + 1 
                                if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 1):
                                        point = point + 5
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point + 5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 20
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point + 5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 1
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 3

                            if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2) and  ( data_pre_race["距離"][tmp] == tend.getGround(500) or data_pre_race["距離"][tmp] == tend.getGround(600) or data_pre_race["距離"][tmp] == tend.getGround(700) or data_pre_race["距離"][tmp] == tend.getGround(800) )):
                                point_cnt = point_cnt + 1 
                                
                                if(int(data_pre_race["着順"][tmp]) <= 5 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 3):
                                        point = point + 20
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point+5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 30
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point+5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 2


                            elif(data_pre_race["距離"][tmp] == tend.getGround(500) or data_pre_race["距離"][tmp] == tend.getGround(600) or data_pre_race["距離"][tmp] == tend.getGround(700) or data_pre_race["距離"][tmp] == tend.getGround(800)):
                                point_cnt = point_cnt + 1 
                                if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                    point = point + 10
                                    if(int(data_pre_race["着順"][tmp]) <= 1):
                                        point = point + 5
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                            point = point + 5
                                        if(int(data_pre_race["着順"][tmp]) <= 1):
                                            point = point + 20
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) == 0):
                                                point = point + 5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 2):
                                                point = point + 1
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][tmp])[-1]) - int(data_pre_race["着順"][tmp]) >= 5):
                                                            point = point + 3






                except:
                    point = point

        # 勝率調査        
            if(case == 3):
                try: 
                    for tmp in range(0,len(data_pre_race),1):
                        try:
                            if(data_pre_race["着順"][tmp]!="除" and data_pre_race["着順"][tmp]!="中" and data_pre_race["着順"][tmp]!="取"):
                                if(data_pre_race["レース名"][tmp].endswith('(G', 0, len(data_pre_race["レース名"][tmp])-2)):
                                    point_cnt = point_cnt + 1 
                                    if(int(data_pre_race["着順"][tmp]) <= 5 ):
                                        point = point + 19
                                        if(int(data_pre_race["着順"][tmp]) <= 3):
                                            point = point + 20
                                            if(int(data_pre_race["着順"][tmp]) <= 1):
                                                point = point + 10

                                else:
                                    point_cnt = point_cnt + 1 
                                    if(int(data_pre_race["着順"][tmp]) <= 3 ):
                                        point = point + 9
                                        if(int(data_pre_race["着順"][tmp]) <= 2):
                                            point = point + 20
                                            if(int(data_pre_race["着順"][tmp]) <= 1):
                                                point = point + 10
                        except:
                            continue

                except:

                    print(name,"err")
                    print(data_pre_race)
                    point = point
                    
            #上り        
            if(case == 4):
                
                point = 0
                maxTime = 0
                
                try: 
                    for tmp in range(0,len(data_pre_race),1):
                        try:
                            if(data_pre_race["着順"][tmp]!="除" and data_pre_race["着順"][tmp]!="中" and data_pre_race["着順"][tmp]!="取"):
                                if(data_pre_race["距離"][tmp] == tend.getGround(0)):
                                    value = 35.5 - float(data_pre_race["上り"][tmp])
                                    if(value > maxTime):
                                        point = value

                                
                        except:
                            continue

                except:
                    print(name,"err")
                    print(data_pre_race)
                    point = point
                    
                    
            #タイム      
            if(case == 5):
                
                point = 0
                maxTime = 0
                
                try: 
                    for tmp in range(0,len(data_pre_race),1):
                        try:
                            if(data_pre_race["着順"][tmp]!="除" and data_pre_race["着順"][tmp]!="中" and data_pre_race["着順"][tmp]!="取"):
                                if(data_pre_race["距離"][tmp] == tend.getGround(0)):
                                    value = (data_pre_race["タイム"][tmp])
                                    data = re.findall("[0-9]",value)
                                    time = int(data[0])*60 + int(data[1])*10 + int(data[2]) + int(data[0])*0.1
                                    
                                    #値を受け取らないといけないです。
                                    checker = tend.df_order6["time"][0] - time
                                    if(checker > maxTime):
                                        point = checker
                                    
                                    
                                
                        except:
                            continue

                except:

                    print(name,"err")
                    print(data_pre_race)
                    point = point





            test_len = len(data_pre_race)
            
            

            return point / point_cnt 


    def vlookup(self,case,value):
        result = 0
        
        if(case == 1):
            for number,average in zip(self.data_horse["name"],self.data_horse["前走"]):
                try: 
                    if(number == value):
                        result = average
                        break
                except:
                    continue    
        

        elif(case == 2):
            for number,average in zip(self.data_horse["name"],self.data_horse["適正"]):
                try: 
                    if(number == value):
                        result = average
                        break
                except:
                    continue

        elif(case == 3):
            for number,average in zip(self.data_horse["name"],self.data_horse["能力"]):
                try: 
                    if(number == value):
                        result = average
                        break
                except:
                    continue
                    
        elif(case == 4):
            for number,average in zip(self.data_horse["name"],self.data_horse["上り"]):
                try: 
                    if(number == value):
                        result = average
                        break
                except:
                    continue
        
        elif(case == 5):
            for number,average in zip(self.data_horse["name"],self.data_horse["タイム"]):
                try: 
                    if(number == value):
                        result = average
                        break
                except:
                    continue

        
        return result



class Tend:
    def __init__(self,name,log_ground,log_meter):
        file_name = name + log_ground + log_meter
        self.log_ground = log_ground
        self.log_meter = log_meter
        self.ground = log_ground + log_meter
        self.df_order = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet1")
        self.df_order2 = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet2")
        self.df_order3 = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet3")
        self.df_order4 = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet4")
        self.df_order5 = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet5")
        self.df_order6 = pd.read_excel("../race_exp/" + file_name + ".xlsx","sheet6")
    
        self.data_exp = pd.read_excel("../race_exp_result/" + file_name + ".xlsx","sheet1")
        self.data_demo = pd.read_excel("../race_demo/" + file_name + ".xlsx","sheet1")
        self.data_odds = pd.read_excel("../race_demo/" + file_name + ".xlsx","sheet3")
        

        
    
    def getGround(self,plus):
        return self.log_ground + str(int(self.log_meter) + plus)
    
    def vlookup(self,case,value):
        result = 0
        if(case == 1):
            for number,average in zip(self.df_order["Unnamed: 0.1"],self.df_order["枠勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
        elif(case == 2):
            for number,average in zip(self.df_order["Unnamed: 0.1"],self.df_order["年齢勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue      

        elif(case == 3):
            for number,average in zip(self.df_order["Unnamed: 0.1"],self.df_order["人気勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue    
        elif(case == 4):
            for number,average in zip(self.df_order2["name"],self.df_order2["勝率"]):
                try: 

                    if(number.startswith(value,0,len(number))):
                                result = average
                                break
                except:
                    continue    

        elif(case == 5):
            for number,average in zip(self.df_order["Unnamed: 0.1"],self.df_order["馬番勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue    
        

        

        elif(case == 6):
            for number,average in zip(self.df_order3["name"],self.df_order3["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
                    
        elif(case == 7):
            for number,average in zip(self.df_order4["name"],self.df_order4["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
                    
        elif(case == 8):
            for number,average in zip(self.df_order5["name"],self.df_order5["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
                    
                    
                    
        return result
    
    

    
    def exp_check(self,value):
        return value
        
        
    def changeTend(self):
        for i in range(0,len(self.df_order),1):    
            if(self.df_order["枠勝率"][i] != "nan"):
                self.df_order["枠勝率"][i] = str(self.df_order["枠勝率"][i])[0:4] + "%"
            if(self.df_order["年齢勝率"][i] != "nan"):   
                self.df_order["年齢勝率"][i] = str(self.df_order["年齢勝率"][i])[0:4] + "%"
            if(self.df_order["人気勝率"][i] != "nan"):
                self.df_order["人気勝率"][i] = str(self.df_order["人気勝率"][i])[0:4] + "%"
            if(self.df_order["馬番勝率"][i] != "nan"):
                self.df_order["馬番勝率"][i] = str(self.df_order["馬番勝率"][i])[0:4] + "%"

        self.df_order.drop(["枠","年齢","人気","馬番","Unnamed: 0"],axis = 1,inplace = True)



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
main.createOutput()
main.createTable2()
main2 = Output(url)
main2.createOutput()

tend.changeTend()

word = pd.read_html(url,header = 1)[0]
word.drop(["枠","性齢","馬体重(増減)","印","厩舎","Unnamed: 9","登録","メモ","斤量","騎手"],axis = 1,inplace = True)
word["ランク"] = 0

for i in range(0,len(main.result),1):
    word["ランク"][i] = main2.result["斤量値"][i] + main2.result["前走"][i] + main2.result["馬実績"][i] + main2.result["馬血統"][i] + main2.result["上り"][i] 
    
words = pd.read_html(url,header = 1)[0]
words.drop(["枠","性齢","馬体重(増減)","印","厩舎","Unnamed: 9","登録","メモ","斤量","馬名"],axis = 1,inplace = True)
words["ランク"] = 0

for i in range(0,len(main.result),1):
    words["ランク"][i] = str(main2.result["騎手（このレース）"][i])[0:5]+"%"


with pd.ExcelWriter("../result/"+output_name+'.xlsx') as writer:
    tend.df_order.to_excel(writer, sheet_name='傾向')
    word.to_excel(writer, sheet_name='競走馬')
    words.to_excel(writer, sheet_name='騎手')
    tend.data_demo.to_excel(writer, sheet_name='デモ結果')
    tend.data_odds.to_excel(writer, sheet_name='配当')
    main.result.sort_values('指数', ascending=False).to_excel(writer, sheet_name='最終結果')
    
    
#最大表示行数の指定（ここでは300行を指定）
# pd.set_option('display.max_rows', 300)
# print("ルメールとデムーロを確認しなさい")
# print("--------------------------------")
# print(words)
# print("--------------------------------")
# print(tend.df_order2)
# print("--------------------------------")


# In[ ]:




