import requests
import json
import sqlite3
import time
class Database(object):
    name=''
    code1=''
    keyvalue = {}  # request的时间参数
    code = ''      # 改变的时间参数
    year_list=[]  #年份的列表
    data_list=[]  #数据的列表
    def __init__(self, name, code1, year_list, data_list, keyvalue, code):
        self.name = name
        self.code1 = code1
        self.year_list = year_list
        self.data_list = data_list
        self.keyvalue = keyvalue
        self.code = code

    def gettime(self):  # 获取时间戳
        return int(round(time.time() * 1000))

    def changekeyvalue(self):  # 改变时间参数
        self.keyvalue['dfwds'] = self.code

    def getvalue(self):  # 得到参数值
        headers = {}
        url = 'http://data.stats.gov.cn/easyquery.htm'
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
 \
                                'AppleWebKit/537.36 (KHTML, like Gecko)' \
 \
                                'Chrome/70.0.3538.102 Safari/537.36'

        self.keyvalue['m'] = 'QueryData'
        self.keyvalue['dbcode'] = 'hgnd'
        self.keyvalue['rowcode'] = 'zb'
        self.keyvalue['colcode'] = 'sj'
        self.keyvalue['wds'] = '[]'
        self.keyvalue['dfwds'] = '[{"wdcode":"zb","valuecode":"A0301"}]'
        self.keyvalue['k1'] = str(self.gettime())
        s = requests.session()
        # 在Session基础上进行一次请求
        r = s.get(url, params=self.keyvalue, headers=headers)
        # 修改dfwds字段内容
        # self.keyvalue['dfwds'] = '[{"wdcode":"sj","valuecode":"LAST20"}]'
        self.changekeyvalue()
        # 再次进行请求
        r = s.get(url, params=self.keyvalue, headers=headers)
        return r  # 返回得到的数据


    def save(self): #将download的数据保存在本地数据库中并读取出来保存到year_list1和population_list中
        year = []
        data = []
        datatext ={}
        if (self.year_list == []):
            datatext = json.loads(self.getvalue().text)
            data_one = datatext['returndata']['datanodes']

            for value in data_one:
                if (self.code1 in value['code']):
                    year.append(value['code'][-4:])
                    if value['data']['strdata'] == '':
                        data.append(int(0))
                    else:
                        data.append(int(value['data']['strdata']))

        #保存到数据库
        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        try:
            cursor.execute('create table databaselist(year varchar(20) primary key, data int)')
            print("created new table databaselist")
        except:
            pass
        try: #在数据库的表中逐个插入数据
            for (years, datas) in zip(year, data):
                insert_cmd = 'insert into databaselist (year,data) values (%s,%d)' % (years, datas)
                cursor.execute(insert_cmd)
        except:
            pass
        cursor.rowcount
        #从数据库中读取数据
        database_list = list(cursor.execute('select * from databaselist'))#得到tuple型数据
        cursor.close()
        conn.commit()
        conn.close()
        year_list1 = []
        data_list1 = []
        for names in database_list:
            year_list1.append(names[0])
            data_list1.append(names[1])
        self.year_list = list(reversed(year_list1))
        self.data_list = list(reversed(data_list1))