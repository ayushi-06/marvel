# Initialise the parser
import argparse
from webbrowser import get
import requests
import json
import pandas as pd
from pprint import pprint as pp
#from mypackage import FuntionModule
parser = argparse.ArgumentParser(description='Provide the api key, hash key, initial letter')

parser.add_argument('api_key', type=str, help ='Provide public key')
parser.add_argument('hash_key', type=str, help ='Provide hash key for authorization')
parser.add_argument('character', type=str, help ='Provide initials of character you wish to fetch')

args=parser.parse_args()
public_key=getattr(args,'api_key')
hash_key =getattr(args,'hash_key')
startswithletter=getattr(args,'character').lower()

def fun_create_df(api,hash):
        header={'response content type':'application/json'}
        offsets = {0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400}
        l=[]
        for o in offsets:
            params={'ts':str(1), 'apikey':api, 'hash': hash,'offset':o, 'limit':100}
            res=requests.get('http://gateway.marvel.com/v1/public/characters', headers=header, params= params)
            #res.raise_for_status()
            res_json =res.json() ## to get result in json format
        
        for item in res_json['data']['results']:
             #setting default values:
            d={'id':0, 'name':'', 'comics':0, 'stories':0, 'events':0,'series':0}
            #setting actual values:
            d['id']= item['id']
            d['name']=item['name']
            d['comics']=item['comics']['available']
            d['stories']=item['stories']['available']
            d['events']=item['events']['available']
            d['series']=item['series']['available']
            l.append(d)
        df=pd.DataFrame(l)
        return df
def filter_fun( df, col,condition,value):
    if col == 'name':
        condition ='start_with'
        length=len(value)
        return(df[df.name.str[:length]==value])
    else:
        if condition=='>':
            dataframe2= df[df[col]> value]
        elif condition =='<':
            dataframe2= df[df[col]< value]
        elif condition =='=':
            dataframe2= df[df[col]== value]
        else:
            print('Invalid condition')
        return dataframe2



df1 = fun_create_df(public_key,hash_key)     
df2 = filter_fun(df1,"events",">",20)
