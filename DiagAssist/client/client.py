import json
import requests
import time

configUrl = 'http://192.168.1.147:8080/api/v3/da/config'

def get(url,data=None):
    reqinfo = {'clientid': '1', 'client_detail_id': '1', 'accesskey': '123ABC','request_data':{"test":"111","subjective_symptoms":"111"}}
    textmod = json.dumps(reqinfo)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    res = requests.get(url,params=reqinfo)
    print(res.headers)
    print(res.status_code)
    print(res.text)
    return res.text

def post(url,data=None):
    reqinfo = {"accesskey":"123ABC","client_detail_id":"1","clientid":"23","request_data":{"only_search_myshop":1,"query_infos":[{"key":"customer.identity","value":"8"}],"range":{"length":100,"location":0}}}
    textmod = json.dumps(reqinfo)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    res = requests.post(url,json=reqinfo,verify=False)
    print(res.text)
    print(res.headers)
    # print(res.status_code)
    if res.text == None :
        exit(0)
        print("errr----------------------------------------------------------errrrrrrrrr")
    return res.text

def put(url,data=None):
    reqinfo = {'clientid': '1', 'client_detail_id': '1', 'accesskey': '123ABC'}
    textmod = json.dumps(reqinfo)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    res = requests.put(url,json=reqinfo)
    print(res.headers)
    print(res.status_code)
    print(res.text)
    return res.text


#post(configUrl)
# get(configUrl)
#put(configUrl)
while True:
    time.sleep(0.5)
    post(url="https://hp.repeatlink.co.jp/RLASP6_MUSE/terminal/v2/cr/mng/QueryCustomers")
