from operator import index
from re import A
import requests
from bs4 import BeautifulSoup
from lxml import html
import pandas as pd
import json
import csv
from pandas import json_normalize

from soupsieve import select

'''
================ [data] =========================
'''

USERE = '********'
PASSWORD = '********'
LOGIN_URL = 'https://aais5.nkust.edu.tw/selcrs_std/Login'
getToken_url = 'https://aais5.nkust.edu.tw/selcrs_std/'
Cookies_header = ''
Cookies_firstSelect = ''

'''
================= [Find Token] ========================
'''

session_requests = requests.session()
result = session_requests.get(getToken_url)
tree = html.fromstring(result.text)
RequestVerificationToken = list(
    set(tree.xpath('//input[@name="__RequestVerificationToken"]/@value')))[0]

'''
==================== [Post login] =====================
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
    # ,'Cookies' : Cookies_firstSelect
}
payload = {
    'UserAccount': USERE,
    'Password': PASSWORD,
    '__RequestVerificationToken': RequestVerificationToken
}

result = session_requests.post(LOGIN_URL, data=payload, headers=headers)

# print(result.headers)

'''
================== [post selWeight] ========================
'''

def SelWeight(SelectCode , scr): # 代碼 課號
    first_select = 'https://aais5.nkust.edu.tw/selcrs_std/FirstSelect/SelectPage' #find Token
    getpre = 'https://aais5.nkust.edu.tw/selcrs_std/Course/GetPreSeleNumber' #post url
    
    response = session_requests.get(
        first_select, headers=dict(referer=first_select))
    
    tree = html.fromstring(response.text)
    RequestVerificationToken_2 = list(set(tree.xpath('//input[@name="__RequestVerificationToken"]/@value')))[0]

    post_data = {  # 權重post資料
        'SelectCode': SelectCode,
        '__RequestVerificationToken': RequestVerificationToken_2
    }

    headers_first = { #初選頁面cookies
        'Cookies': Cookies_firstSelect
        }

    result2 = session_requests.post(getpre, data=post_data, headers=headers_first)
    list_of_dicts = result2.json()

    SelOrd = [] #志願序
    SelWeight = [] #權重
    SelCount = [] #人數
    all = 0
    all_list = [] #累積人數
    scr_precnt = findprecnt(scr) #限修人數
    myW = list_of_dicts.get("SelWeight")
   
    print('課名 : ' , findname(scr))
    print('限修人數 :' , scr_precnt )
    print('我的權重 :' , myW)
    
    for i in list_of_dicts.get('data'):
        for k, v in i.items():
            if k == 'SelOrd': #志願
                SelOrd.append(v)
            elif k == 'SelWeight': #權重
                SelWeight.append(v)
            elif k == 'SelCount': #人數
                all = all + v
                all_list.append(all)
                SelCount.append(v)         
            
    result_df = pd.DataFrame({'志願序': SelOrd, '權重': SelWeight,
                              '人數': SelCount, '累積人數': all_list })
    result_df.index = result_df['志願序']
    result_df = result_df.drop('志願序' , axis = 1)
    print(result_df)
    result_df.to_csv(f"{findname(scr)}.csv") #輸出檔名為課名的csv

def findselcode(scr_selcode):#輸入課號 >> code
    df = pd.read_csv('AllData.csv' ,  index_col=[0])
    return df.loc[scr_selcode][1]

def findprecnt(scr_selcode):#輸入課號 >> 人數
    df = pd.read_csv('AllData.csv' ,  index_col=[0])
    return df.loc[scr_selcode][0]

def findname(scr_selcode):#輸入課號 >> 課名
    df = pd.read_csv('AllData.csv' ,  index_col=[0])
    return df.loc[scr_selcode][2]

# def findSeltype(): #輸入課號 >> 必選修代碼 (M , O)
#     df = pd.read_csv('AllData.csv' ,  index_col=[0])
#     return df.loc[scr_selcode][2]
  
def findPcrs_no(scr_selcode): #輸入課號 >> 加選代碼 
    df = pd.read_csv('AllData.csv' ,  index_col=[0])
    return df.loc[scr_selcode][3]


'''
============================[main]===================================
'''

seltype = 'M'

scr_selcode = int(input('輸入課號 : '))
SelWeight(findselcode(scr_selcode) , scr_selcode)

# pcrs_no = findPcrs_no(scr_selcode)
# addcrs(pcrs_no , scr_selcode , seltype)


'''
==========================[test code]=================================
'''
# def addcrs(pcrs_no , scr_selcode , seltype): #加選
#     add_url = 'https://aais5.nkust.edu.tw/selcrs_std/AddSelect/AddSelectCrs'
#     post_data = 'CrsNo=2177&PCrsNo=138C00053&SelType=M'
#     headers_add = {
#         'cookie' : ''
#     }
#     result = session_requests.post(add_url, data=post_data, headers=headers_add)
#     # list_of_dicts = result.json()
#     print(result.status_code , result.text)

# def probability():
