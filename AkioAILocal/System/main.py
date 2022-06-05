class Race:
    def __init__(self,log_place,log_cord,log_ground,log_meter,src,road,url_topic):
        self.log_place = log_place
        self.log_cord = log_cord
        self.log_ground = log_ground
        self.log_meter = log_meter
        self.src = src
        self.road = road
        self.url_topic = url_topic;
        
        
        self.data_max = pd.DataFrame([ [0]],
                    columns = ["max"],
                    index = [1])
        self.data_max["max"][1] = 0
        
        self.maxinfoExp = pd.DataFrame([ [1,0]],
                    columns = ["max","min"],
                    index = ["a","b","c","d","e","f","g","h","k"])
        
        
#         トピックのurlを返す
    def get_topic(self):
        return self.race_id_list       
        
        
#         指定されたコースのurlを返す
    def get_link(self):
        return self.race_id_lists
    
#     指定されたコースurl更新
    def set_link(self,changeUrl):
        self.race_id_lists = changeUrl
    
    
    def get_link_exp(self):
        return self.race_id_lists_exp
    
    
    def get_url_topic(self):
        return self.url_topic
    
    def get_preser_name(self):
        return self.preser_name
        
    
    
    
    
    
#     馬場と距離を返す。距離適正で使う
    def get_ground(self,plus):
        return self.log_ground + str(int(self.log_meter) + plus)
    
    
    def getURLTopic(self):
        #         トピックのurl取得
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

    
        
    def get_url(self):
                
#         指定されたコースのurl取得
        self.race_id_lists = []
        for age in tqdm(range(2000,2020,1)):
            for place in range(self.log_cord,self.log_cord+1,1):
                for kai in (range(1,6,1)):
                    for day in range(1,9,1):     
                         for r in range(11,12,1):
                            try:

                                race_id = "https://db.netkeiba.com/race/"+ str(age).zfill(2) + str(place).zfill(2) + str(kai).zfill(2) + str(day).zfill(2)+ str(r).zfill(2)+  "/"
                                url = race_id
                                df = pd.read_html(url)[0]

                                response = requests.get(url)
                                response.encoding = "EUC-JP"
                                soup = BeautifulSoup(response.text, 'html.parser')
                                ul = soup.find('ul',class_ = "race_place fc")
                                filed = ul.find('a',class_ = "active") 
                                x = str(filed)[45:47]  

                                df = pd.read_html(url)[0]

                                response = requests.get(url)
                                response.encoding = "EUC-JP"
                                soup = BeautifulSoup(response.text, 'html.parser')
                                div = soup.find('div',class_ = "data_intro")
                                filed = div.find('span')   
                                y = str(filed)[6:14]
                                
                                if(x == self.log_place and y.startswith(self.log_ground,0,len(y)) and y.startswith(self.road,1,len(y)) and y.startswith(self.log_meter,self.src,len(y))):
                                    self.race_id_lists.append(race_id)  
                            except:
                                continue



class Tend:

    def __init__(self):
        
        self.averageTime = 0
        self.averageTimeCnt = 0
        
        
        
        
        self.data_frame = pd.DataFrame([ [0,0,0,0,0,0,0,0]],
                    columns = ["枠","枠勝率","年齢","年齢勝率","人気","人気勝率","馬番","馬番勝率"],
                    index = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18])
        self.data_jockey = pd.DataFrame({'name':[],
                                        'cnt':[],
                                        '勝率':[],
                                        })
        self.data_blood = pd.DataFrame({'name':[],
                                        'cnt':[],
                                        '勝率':[],
                                        })
        self.data_prev = pd.DataFrame({'name':[],
                                        'cnt':[],
                                        '勝率':[],
                                        })
        
        self.timeInfo = pd.DataFrame([ [0]],
                        columns = ["time"],
                        index = [1])
        
        
    def getAverageTime(self):
        return self.averageTime / self.averageTimeCnt
    
    
    #timeの値をセッティング
    def setTime(self):
        self.timeInfo.loc[1,"time"] = self.getAverageTime()
    


    def create_tend(self,race_id_lists):
        
        for i in (range(0,len(race_id_lists),1)):

            try:
                url = race_id_lists[i]
                dfs = pd.read_html(url)[0]
                data = pd.read_html(url,header=0)[0]
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                table = soup.find('table')
                links = []
                for tr in table.findAll("tr"):

                    try:
                        link = tr.find_all(href=re.compile("^/horse"))

                        if(len(link) != 0):
                            link = "https://db.netkeiba.com" + str(link)[10:28]
                            links.append(link)

                    except:
                        pass
                data['HorseLink'] = links  
                
                #日時の保存
                response = requests.get(url)
                response.encoding = "EUC-JP"
                soup = BeautifulSoup(response.text, 'html.parser')
                div = soup.find('div',class_ = "race_head_inner")
                li = div.find('li',class_ = "result_link")
                z =str(li)
                z = z[55:59] + "/" + z[60:62] + "/" + z[63:65]


    #血統と前走を保存
                blood_1 = []
                blood_2 = []
                prev_game = []
                for x in data['HorseLink']:
                    blood = pd.read_html(x)[2]
                    blood_1.append(blood[0][0])
                    blood_2.append(blood[1][2])
                    
                    game = pd.read_html(x)[3]
                    for cnt_age in range(0,len(game),1):

                        if (game["日付"][cnt_age].startswith(z,0,len(game["日付"][cnt_age])) ):
                            break
                        
                    prev_game.append(game["レース名"][cnt_age+1])
                    
                    
                data['blood_1'] = blood_1
                data['blood_2'] = blood_2
                data['前走大会'] = prev_game

            except:
                continue
                
                
            for x,y,z,n,p,j,un,bl_1,bl_2,pg,tm in zip(data['着順'],data['枠番'],data['馬名'],data['性齢'],data["人気"],data['騎手'],data['馬番'],data['blood_1'],data['blood_2'],data['前走大会'],data['タイム']):
                try:
                    flg = 0
                    for ab in self.data_jockey["name"]:
                        if(ab == j):
                            flg = 1
                            break


                    if(flg == 1):
                        self.data_jockey.loc[j,"勝率"] = self.data_jockey.loc[j,"勝率"]+1

                    else:
                        self.data_jockey.loc[j,:]= [j,0,1]




                    flg = 0
                    for ab in self.data_blood["name"]:
                        if(ab == bl_1):
                            flg = 1
                            break

                    if(flg == 1):
                        self.data_blood.loc[bl_1,"勝率"] = self.data_blood.loc[bl_1,"勝率"]+1

                    else:
                        self.data_blood.loc[bl_1,:]= [bl_1,0,1]


                    flg = 0
                    for ab in self.data_blood["name"]:
                        if(ab == bl_2):
                            flg = 1
                            break


                    if(flg == 1):
                            self.data_blood.loc[bl_2,"勝率"] = self.data_blood.loc[bl_2,"勝率"]+1

                    else:
                        self.data_blood.loc[bl_2,:]= [bl_2,0,1]
                        
                        
                    flg = 0
                    for ab in self.data_prev["name"]:
                        if(ab == pg):
                            flg = 1
                            break


                    if(flg == 1):
                            self.data_prev.loc[pg,"勝率"] = self.data_prev.loc[pg,"勝率"]+1

                    else:
                        self.data_prev.loc[pg,:]= [pg,0,1]



                        
                        

                    if(int(x) <= 3):
                        self.data_frame.loc[y,"枠"] = self.data_frame.loc[y,"枠"] + 1
                        self.data_frame.loc[int(n[1]),"年齢"] = self.data_frame.loc[int(n[1]),"年齢"] +1
                        self.data_frame.loc[p,"人気"] = self.data_frame.loc[p,"人気"] + 1
                        self.data_frame.loc[un,"馬番"] = self.data_frame.loc[un,"馬番"] + 1
                        
                        #タイム計測
                        data = re.findall("[0-9]",tm)
                        time = int(data[0])*60 + int(data[1])*10 + int(data[2]) + int(data[0])*0.1
                        self.averageTime = self.averageTime + time
                        self.averageTimeCnt = self.averageTimeCnt + 1
                        

                        
                        #jockey更新
                        flg = 0
                        for ab in self.data_jockey["name"]:
                            if(ab == j):
                                flg = 1
                                break


                        if(flg == 1):
                            self.data_jockey.loc[j,"cnt"] = self.data_jockey.loc[j,"cnt"]+1



                        #血統更新1
                        flg = 0
                        for ab in self.data_blood["name"]:
                            if(ab == bl_1):
                                flg = 1
                                break


                        if(flg == 1):
                            self.data_blood.loc[bl_1,"cnt"] = self.data_blood.loc[bl_1,"cnt"]+1

                        #血統更新2
                        flg = 0
                        for ab in self.data_blood["name"]:
                            if(ab == bl_2):
                                flg = 1
                                break


                        if(flg == 1):
                            self.data_blood.loc[bl_2,"cnt"] = self.data_blood.loc[bl_2,"cnt"]+1
                            
                        #前走更新
                        flg = 0
                        for ab in self.data_prev["name"]:
                            if(ab == pg):
                                flg = 1
                                break


                        if(flg == 1):
                            self.data_prev.loc[pg,"cnt"] = self.data_prev.loc[pg,"cnt"]+1




                    self.data_frame.loc[y,"枠勝率"] = self.data_frame.loc[y,"枠勝率"] + 1
                    self.data_frame.loc[un,"馬番勝率"] = self.data_frame.loc[un,"馬番勝率"] + 1
                    self.data_frame.loc[p,"人気勝率"] = self.data_frame.loc[p,"人気勝率"] + 1
                    self.data_frame.loc[int(n[1]),"年齢勝率"] = self.data_frame.loc[int(n[1]),"年齢勝率"] + 1

                except:
                    continue




        for i,j in zip(self.data_jockey["cnt"],self.data_jockey["name"]):
            self.data_jockey.loc[j,"勝率"] = (self.data_jockey.loc[j,"cnt"] / self.data_jockey.loc[j,"勝率"])*100


        for i,j in zip(self.data_blood["cnt"],self.data_blood["name"]):
            self.data_blood.loc[j,"勝率"] = (self.data_blood.loc[j,"cnt"] / self.data_blood["cnt"].sum())*100

        for i,j in zip(self.data_prev["cnt"],self.data_prev["name"]):
            self.data_prev.loc[j,"勝率"] = (self.data_prev.loc[j,"cnt"] / self.data_prev["cnt"].sum())*100


            
            
            
        for i in range(1,len(self.data_frame)+1,1):
            self.data_frame.loc[i,"枠勝率"] = (self.data_frame.loc[i,"枠"] / self.data_frame.loc[i,"枠勝率"])*100
            self.data_frame.loc[i,"年齢勝率"] = (self.data_frame.loc[i,"年齢"] / self.data_frame.loc[i,"年齢勝率"])*100
            self.data_frame.loc[i,"人気勝率"] = (self.data_frame.loc[i,"人気"] / self.data_frame.loc[i,"人気勝率"])*100 
            self.data_frame.loc[i,"馬番勝率"] = (self.data_frame.loc[i,"馬番"] / self.data_frame.loc[i,"馬番勝率"])*100 





        with pd.ExcelWriter("log.xlsx") as writer:
            self.data_frame.to_excel(writer, sheet_name='sheet1')
            self.data_jockey.to_excel(writer, sheet_name='sheet2')
            self.data_blood.to_excel(writer, sheet_name='sheet3')
            self.data_prev.to_excel(writer, sheet_name='sheet4')



        self.data_frame = pd.read_excel("log.xlsx","sheet1")
        self.data_jockey = pd.read_excel("log.xlsx","sheet2")
        self.data_blood= pd.read_excel("log.xlsx","sheet3")
        self.data_prev= pd.read_excel("log.xlsx","sheet4")
        # race_name = dfs["レース名"][0]    


    def vlookup(self,case,value):
        result = 0
        if(case == 1):
            for number,average in zip(self.data_frame["Unnamed: 0"],self.data_frame["枠勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
        elif(case == 2):
            for number,average in zip(self.data_frame["Unnamed: 0"],self.data_frame["年齢勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue      

        elif(case == 3):
            for number,average in zip(self.data_frame["Unnamed: 0"],self.data_frame["人気勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue    
        elif(case == 4):
            for number,average in zip(self.data_jockey["Unnamed: 0"],self.data_jockey["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue    

        elif(case == 5):
            for number,average in zip(self.data_frame["Unnamed: 0"],self.data_frame["馬番勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue


        elif(case == 6):
            for number,average in zip(self.data_blood["name"],self.data_blood["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
                    
        elif(case == 7):
            for number,average in zip(self.data_prev["name"],self.data_prev["勝率"]):
                try: 
                    if(number == value):
                                result = average
                                break
                except:
                    continue
        return result

    
    def fixJockey(self):
        for i in range(0,len(self.data_jockey),1):
            if(self.data_jockey["cnt"][i] == 1 and self.data_jockey["勝率"][i] == 100):
                self.data_jockey.loc[i,"勝率"] = 49.625
                
            if(self.data_jockey["cnt"][i] == 2 and self.data_jockey["勝率"][i] == 100):
                self.data_jockey.loc[i,"勝率"] = 66.25
                
            if(self.data_jockey["cnt"][i] == 1 and self.data_jockey["勝率"][i] == 50):
                self.data_jockey.loc[i,"勝率"] = 33
                
            if(self.data_jockey["cnt"][i] == 3 and self.data_jockey["勝率"][i] == 100):
                self.data_jockey.loc[i,"勝率"] = 83
                
            if(self.data_jockey["cnt"][i] == 2 and self.data_jockey["勝率"][i] == 66.6666666666667):
                self.data_jockey.loc[i,"勝率"] = 49.5
            
            if(self.data_jockey["cnt"][i] == 1 and self.data_jockey["勝率"][i] == 33.3333333333333):
                self.data_jockey.loc[i,"勝率"] = 16.5
                
            if(self.data_jockey["Unnamed: 0"][i] == "Ｍ．デム"):
                self.data_jockey.loc[i,"Unnamed: 0"] = "Ｍデムーロ"
                self.data_jockey.loc[i,"name"] = "Ｍデムーロ"
                



class Horse:
    def __init__(self):
        self.data_horse = pd.DataFrame({
                                'name':[],
                                '前走':[],
                                '適正':[],
                                '能力':[],
                                '上り':[],
                                'タイム':[],
                                })
        
        
    def pre_race(self,case,age,data_pre_race):
        
        point = 1
        point_cnt = 1
    #     前走を評価
        if(case == 1):


            try: 
                for cnt_age in range(0,len(data_pre_race),1):

                    if (data_pre_race["日付"][cnt_age].startswith(age,0,len(data_pre_race["日付"][cnt_age])) ):
                        break

               


                if( data_pre_race["着順"][cnt_age + 1]!="除" and data_pre_race["着順"][cnt_age + 1]!="中" and data_pre_race["着順"][cnt_age + 1]!="取" ):
                    if(data_pre_race["レース名"][cnt_age + 1].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + 1])-2)): 
                        point = point + 14
                        if(int(data_pre_race["着順"][cnt_age + 1]) <= 8 ):
                            point = point + 15
                            if(int(data_pre_race["着順"][cnt_age + 1]) <= 3):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + 1]) <= 1):
                                    point = point + 10


                    else:

                        if(int(data_pre_race["着順"][cnt_age + 1]) <= 3 ):
                            point = point + 10
                            if(int(data_pre_race["着順"][cnt_age + 1]) <= 2):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + 1]) <= 1):
                                    point = point + 10

            except:
                return 0




    #     距離適正を評価       
        if(case == 2):
            try:
                for cnt_age in range(0,len(data_pre_race),1):

                    if (data_pre_race["日付"][cnt_age].startswith(age,0,len(data_pre_race["日付"][cnt_age])) ):
            #             print(cnt_age,"番目")
                        break

            #     print(len(data_pre_race[cnt_age:]))     


                for tmp in range(1,len(data_pre_race[cnt_age:]),1):

                    if(data_pre_race["着順"][cnt_age + tmp]!="除" and data_pre_race["着順"][cnt_age + tmp]!="中" and data_pre_race["着順"][cnt_age + tmp]!="取"):
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2) and data_pre_race["距離"][cnt_age + tmp] == race.get_ground(0)):
                            point_cnt = point_cnt + 1
                            point = point + 19 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 8 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 15
                                    
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 25
                                        
                        


                        elif(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(0)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 2):
                                    point = point + 15
    
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 25
                                        



                        
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2) and ( data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-100) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-200) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-300) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-400) )):
                            point_cnt = point_cnt + 1 
                            point = point + 5
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 8 ):
                                point = point + 5
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 15
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 25
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 15
                                            
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                            point = point + 2
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                                point = point + 3
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                    point = point + 4
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                        point = point + 4
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                            point = point + 6


                        elif(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-100) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-200) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-300) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-400)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 5
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                    point = point + 10
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 15
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 15
                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                    point = point + 1
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                            point = point + 2
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                point = point + 4
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                    point = point + 4
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                        point = point + 6               




                        
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2) and ( data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-500) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-600) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-700) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-800) )):
                            point_cnt = point_cnt + 1 
                            point = point + 5
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 8 ):
                                point = point + 5
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 10
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 10
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 20
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 25
                                            
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                        point = point + 4
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                            point = point + 4
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                                point = point + 4
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                    point = point + 8
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                        point = point + 8
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                            point = point + 8


                        elif(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-500) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-600) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-700) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(-800)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 5
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                    point = point + 5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 10
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 10
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 20
                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                    point = point + 4
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                        point = point + 4
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                            point = point + 4
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                point = point + 6
                    
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                    point = point + 6
                                    
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                        point = point + 6               



                                
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2) and ( data_pre_race["距離"][cnt_age + tmp] == race.get_ground(100) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(200) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(300) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(400) )):
                            point_cnt = point_cnt + 1 
                            
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 5 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 20
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 30
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 5 
                                            
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                            point = point + 2


                        elif(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(100) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(200) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(300) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(400)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                    point = point + 5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 20
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 5
                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                    point = point + 1
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                        point = point + 3              



                                
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2) and ( data_pre_race["距離"][cnt_age + tmp] == race.get_ground(500) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(600) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(700) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(800) )):
                            point_cnt = point_cnt + 1 
                            
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 5 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 20
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 30
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 5 
                                            
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                        point = point + 2
                                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                            point = point + 2


                        elif(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(500) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(600) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(700) or data_pre_race["距離"][cnt_age + tmp] == race.get_ground(800)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 10
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                    point = point + 5
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                        point = point + 5
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 20
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) == 0):
                                            point = point + 5
                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 0):
                                    point = point + 1
                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 1):
                                        point = point + 1
                                        if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 2):
                                            point = point + 1
                                            if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 3):
                                                point = point + 2
                                                if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 4):
                                                    point = point + 2
                                                    if( int(re.findall(r'\d+',data_pre_race["通過"][cnt_age + tmp])[-1]) - int(data_pre_race["着順"][cnt_age + tmp]) >= 5):
                                                        point = point + 3              

                                       
                                                        



            except:
                return 0

    #sum調査        
        if(case == 3):
            try: 
                for cnt_age in range(0,len(data_pre_race),1):
                    if (data_pre_race["日付"][cnt_age].startswith(age,0,len(data_pre_race["日付"][cnt_age])) ):
                        break


                for tmp in range(1,len(data_pre_race[cnt_age:])-1,1):
                    if(data_pre_race["着順"][cnt_age + tmp]!="除" and data_pre_race["着順"][cnt_age + tmp]!="中" and data_pre_race["着順"][cnt_age + tmp]!="取"):
                        if(data_pre_race["レース名"][cnt_age + tmp].endswith('(G', 0, len(data_pre_race["レース名"][cnt_age + tmp])-2)):
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 5 ):
                                point = point + 19
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3):
                                    point = point + 20
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 10

                        else:
                            point_cnt = point_cnt + 1 
                            if(int(data_pre_race["着順"][cnt_age + tmp]) <= 3 ):
                                point = point + 9
                                if(int(data_pre_race["着順"][cnt_age + tmp]) <= 2):
                                    point = point + 20
                                    if(int(data_pre_race["着順"][cnt_age + tmp]) <= 1):
                                        point = point + 10

            except:
                return 0
            
            
        #上がり評価
        if(case == 4):
            
            maxTime = 0
            point = 0
            try: 
                for cnt_age in range(0,len(data_pre_race),1):

                    if (data_pre_race["日付"][cnt_age].startswith(age,0,len(data_pre_race["日付"][cnt_age])) ):
                        break

               


                for tmp in range(1,len(data_pre_race[cnt_age:])-1,1):
                    if(data_pre_race["着順"][cnt_age + tmp]!="除" and data_pre_race["着順"][cnt_age + tmp]!="中" and data_pre_race["着順"][cnt_age + tmp]!="取"):
                        if(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(0)):
                            value = 35.5 - float(data_pre_race["上り"][cnt_age + tmp])
                            
                            if(value > maxTime):
                                point = value
                                
                        else:
                            continue
                                         

            except:
                return 0
            
        #タイム評価
        if(case == 5):
            
            maxTime = 0
            point = 0
            
            try: 
                for cnt_age in range(0,len(data_pre_race),1):

                    if (data_pre_race["日付"][cnt_age].startswith(age,0,len(data_pre_race["日付"][cnt_age])) ):
                        break

               


                for tmp in range(1,len(data_pre_race[cnt_age:])-1,1):
                    if(data_pre_race["着順"][cnt_age + tmp]!="除" and data_pre_race["着順"][cnt_age + tmp]!="中" and data_pre_race["着順"][cnt_age + tmp]!="取"):
                        if(data_pre_race["距離"][cnt_age + tmp] == race.get_ground(0)):
                            value = (data_pre_race["タイム"][cnt_age + tmp])
                            data = re.findall("[0-9]",value)
                            time = int(data[0])*60 + int(data[1])*10 + int(data[2]) + int(data[0])*0.1
                            checker = topicTend.getAverageTime() - time
                            if(checker > maxTime):
                                point = checker
               
                return point
                                         

            except:
                return 0
    
            




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




class Exp:
    def __init__(self):
        self.data_exp = pd.DataFrame({
                        'a':[],
                        'b':[],
                        'c':[],
                        'd':[],
                        'e':[],
                        'f':[],
                        'g':[],
                        'h':[],
                        'k':[],
                        'start':[],
                        'length':[],
                        'target':[],
                                }) 
        self.expCnt = 0
        
    def create_exp(self,exp):
        
            
                
        try:


            df = pd.read_html(exp,header=0)[0]
    #馬のリンクを保存
            response = requests.get(exp)
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table')
            links = []
            for tr in table.findAll("tr"):

                try:
                    link = tr.find_all(href=re.compile("^/horse"))
                    if(len(link) == 0):
                        continue

                    link = "https://db.netkeiba.com" + str(link)[10:28]

                    links.append(link)

                except:
                    pass
            df['HorseLink'] = links 
            
            
     #日時の保存
            response = requests.get(exp)
            response.encoding = "EUC-JP"
            soup = BeautifulSoup(response.text, 'html.parser')
            div = soup.find('div',class_ = "race_head_inner")
            li = div.find('li',class_ = "result_link")
            z =str(li)
            z = z[55:59] + "/" + z[60:62] + "/" + z[63:65]
            print(z)



            
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
                    for cnt_age in range(0,len(game),1):

                        if (game["日付"][cnt_age].startswith(z,0,len(game["日付"][cnt_age])) ):
                            break
                    prev_game.append(game["レース名"][cnt_age+1])
                except:
                    game = pd.read_html(x)[4]
                    for cnt_age in range(0,len(game),1):

                        if (game["日付"][cnt_age].startswith(z,0,len(game["日付"][cnt_age])) ):
                            break
                    prev_game.append(game["レース名"][cnt_age+1])
                    
                
                
            df['blood_1'] = blood_1
            df['blood_2'] = blood_2  
            df['前走大会'] = prev_game
            
   
            
            
    
            
       
            

        #horseインスタンス化
            horse = Horse()
            for i in range(0,len(df),1):
                data_pre_race = pd.read_html(df["HorseLink"][i])[3]
                name = df.loc[i]["馬名"]
                horse.data_horse.loc[i,:] = [name,horse.pre_race(1,z,data_pre_race),horse.pre_race(2,z,data_pre_race),horse.pre_race(3,z,data_pre_race),horse.pre_race(4,z,data_pre_race),horse.pre_race(5,z,data_pre_race)]
                if(horse.data_horse["前走"][i] == 0 and horse.data_horse["適正"][i] == 0 and horse.data_horse["能力"][i] == 0):
                    data_pre_race = pd.read_html(df["HorseLink"][i])[4]
                    horse.data_horse.loc[i,:] = [name,horse.pre_race(1,z,data_pre_race),horse.pre_race(2,z,data_pre_race),horse.pre_race(3,z,data_pre_race),horse.pre_race(4,z,data_pre_race),horse.pre_race(5,z,data_pre_race)]
                    if(horse.data_horse["前走"][i] == 0 and horse.data_horse["適正"][i] == 0 and horse.data_horse["能力"][i] == 0):
                        data_pre_race = pd.read_html(df["HorseLink"][i])[5]
                        horse.data_horse.loc[i,:] = [name,horse.pre_race(1,z,data_pre_race),horse.pre_race(2,z,data_pre_race),horse.pre_race(3,z,data_pre_race),horse.pre_race(4,z,data_pre_race),horse.pre_race(5,z,data_pre_race)]

                        
    #         vlookup関数で値を取得
            for i in range(0,len(df),1):
                try:
                    errCheck = 1 + int(df["着順"][i]) 
                    self.data_exp.loc[i + self.expCnt,"a"] =  ( decadeTend.vlookup(1,int(df["枠番"][i])) + decadeTend.vlookup(5,int(df["馬番"][i])) ) / 2
                    self.data_exp.loc[i + self.expCnt,"b"] =  int(df["斤量"][i])
                    self.data_exp.loc[i + self.expCnt,"c"] =  horse.vlookup(2,df["馬名"][i])
                    self.data_exp.loc[i + self.expCnt,"d"] =  (topicTend.vlookup(4,df["騎手"][i]) + decadeTend.vlookup(4,df["騎手"][i]))/2
                    self.data_exp.loc[i + self.expCnt,"e"] =  horse.vlookup(4,df["馬名"][i])
                    self.data_exp.loc[i + self.expCnt,"f"] =  (horse.vlookup(1,df["馬名"][i]) + horse.vlookup(3,df["馬名"][i]))/2
                    self.data_exp.loc[i + self.expCnt,"g"] =  (topicTend.vlookup(6,df["blood_1"][i]) + topicTend.vlookup(6,df["blood_2"][i]))
                    self.data_exp.loc[i + self.expCnt,"h"] =  (topicTend.vlookup(7,df["前走大会"][i]))
                    self.data_exp.loc[i + self.expCnt,"k"] =  horse.vlookup(5,df["馬名"][i])
                    self.data_exp.loc[i + self.expCnt,"target"] = i + 1
                    
#                     開始位置と出走数を保存 
                    if(i == 0):
                        self.data_exp.loc[i + self.expCnt,"start"] = self.expCnt
                        self.data_exp.loc[i + self.expCnt,"length"] = len(df)
                        
                    elif(i == 1):
                        self.data_exp.loc[i + self.expCnt,"start"] = i + self.expCnt -1
                        self.data_exp.loc[i + self.expCnt,"length"] = len(df)
                        
                    elif(i == 2):
                        self.data_exp.loc[i + self.expCnt,"start"] = i + self.expCnt -2
                        self.data_exp.loc[i + self.expCnt,"length"] = len(df)
                        
                        
                    else:
                        self.data_exp.loc[i + self.expCnt,"start"] = 0
                        self.data_exp.loc[i + self.expCnt,"length"] = 0
                    
                    
                    

                except:
                    self.data_exp.loc[i + self.expCnt,"a"] = 0 
                    self.data_exp.loc[i + self.expCnt,"b"] = 0
                    self.data_exp.loc[i + self.expCnt,"c"] = 0
                    self.data_exp.loc[i + self.expCnt,"d"] = 0
                    self.data_exp.loc[i + self.expCnt,"e"] = 0
                    self.data_exp.loc[i + self.expCnt,"f"] = 0
                    self.data_exp.loc[i + self.expCnt,"g"] = 0
                    self.data_exp.loc[i + self.expCnt,"h"] = 0
                    self.data_exp.loc[i + self.expCnt,"k"] = 0
                    self.data_exp.loc[i + self.expCnt,"start"] = 0
                    self.data_exp.loc[i + self.expCnt,"length"] = 0
                    self.data_exp.loc[i + self.expCnt,"target"] = i + 1
                    continue
                    
            
    
            self.expCnt = self.expCnt + len(df)
        except: 
            print("err")


import pandas as pd 
import requests
from bs4 import BeautifulSoup 
import re
from tqdm import tqdm as tqdm
print("競馬場")    
log_place = input()
print("コード入力 札幌:1 東京:5 中山:6 中京:7 阪神:9")
log_cord = int(input())
print("芝 or ダ")
log_ground = input()
print("距離")
log_meter = input()
print("内or外:2 or 4")
src = int(input())  
print("右左")
road = input()
print("topic")
url_topic = input()


# topicからレースurlを取得
race = Race(log_place,log_cord ,log_ground,log_meter,src,road,url_topic)
race.getURLTopic()
race.get_url()
topicURL = race.get_topic()
decadeURL = race.get_link()




# topic分だけ集計
topicTend = Tend()
topicTend.create_tend(topicURL)
topicTend.fixJockey()
topicTend.setTime()




#十年分を集計
decadeTend = Tend()
decadeTend.create_tend(decadeURL)
decadeTend.fixJockey()



#インプット資材作成
main = Exp()
for ageCheck in tqdm(range(0,20,1)):    
    main.create_exp(topicURL[ageCheck])


with pd.ExcelWriter("../race_data/"+log_place+log_ground+log_meter+".xlsx") as writer:
    main.data_exp.to_excel(writer, sheet_name='sheet1')
    

with pd.ExcelWriter("../maxinfo/"+log_place+log_ground+log_meter+".xlsx") as writer:
    race.data_max.to_excel(writer, sheet_name='sheet1')
    race.maxinfoExp.to_excel(writer,sheet_name='sheet2')
    

with pd.ExcelWriter("../race_exp/"+log_place+log_ground+log_meter+".xlsx") as writer:
    decadeTend.data_frame.to_excel(writer, sheet_name='sheet1')
    decadeTend.data_jockey.to_excel(writer, sheet_name='sheet2')
    topicTend.data_blood.to_excel(writer, sheet_name='sheet3')
    topicTend.data_prev.to_excel(writer, sheet_name='sheet4')
    topicTend.data_jockey.to_excel(writer, sheet_name='sheet5')
    topicTend.timeInfo.to_excel(writer,sheet_name='sheet6')


    


