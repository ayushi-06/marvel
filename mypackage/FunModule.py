import hashlib
import requests
import datetime
import json
import pandas as pd
from pprint import pprint as pp
def hasg_params():
    """ Marvel API requires server side API calls to include 
    md5 hash of timestamp + public key + private key"""
    hash_md5=hashlib.md5()
    hash_md5.update((timestamp+private_key+pub_key).encode())
    hashed_params= hash_md5.hexdigest()
    return hashed_params

def fun_create_df(api='944f5f070b59ac0017e57b673e5de6c9',hashkey=hasg_params()):
    timestamp = datetime.datetime.now().strftime('%m/%d/%y %H:%M:%S')
    header={'response content type':'application/json'}
    offsets = {0,100,200,300,400,500,600,700,800,900,1000,1100,1200,1300,1400}
    for o in offsets:
        params={'ts':timestamp, 'apikey':api, 'hash': hashkey,'offset':o, 'limit':100}
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
    