import json
import requests


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
    reqinfo = {'clientid': '1', 'client_detail_id': '1', 'accesskey': '123ABC','request_data':{"subjective_symptoms":"111"}}
    textmod = json.dumps(reqinfo)
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',"Content-Type": "application/json"}
    res = requests.post(url,json=reqinfo)
    print(res.text)
    print(res.headers)
    print(res.status_code)
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
get(configUrl)
#put(configUrl)

