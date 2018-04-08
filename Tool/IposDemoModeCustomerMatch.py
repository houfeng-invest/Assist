
#!/usr/bin/python3
#coding=utf-8

# -------------------------------------------------------------------------------
# Filename:    RLBuildipa3.py
# Revision:    0.1
# Date:        2018/02/26
# Author:      houfeng
# Description: 根据excel里面的顾客名字,把离线json里面的数据进行替换
# -------------------------------------------------------------------------------


import numpy as np
import pandas as pd
import openpyxl
import json

G_CUS_NAME_RESOURCE_DATA = "./customerdemoname.xlsx"
G_CUS_JSON_DATA = './RLCustomerManagementQueryCustomersAction.json'
G_CUS_JSON_DATA_NEW = './RLCustomerManagementQueryCustomersAction1.json'

cus_data_resource = pd.read_excel(G_CUS_NAME_RESOURCE_DATA,header=None)
cus_data_resource.columns = ['fullname','fullnameKana','gender']
#cus_data_resource.drop_duplicates()
print(cus_data_resource.shape)
print(cus_data_resource.head())
cus_data_row = cus_data_resource.shape[0]

print(cus_data_resource.iloc[0]['fullname'])

with open(G_CUS_JSON_DATA,encoding='utf-8') as f:
    cus_json_data = json.load(f)
    index = 0
    for cusInfo in cus_json_data['results']['result_datas']['customers']:
        dataRow = index
        if index >= cus_data_row:
            dataRow = index % cus_data_row
        cus_res = cus_data_resource.iloc[dataRow]
        fullname = cus_res['fullname']
        fullnameKana = cus_res['fullnameKana']
        gender =  cus_res['gender']
        print("match "+ str(index+1) + " customer")
        cus = cusInfo['customer']
        if 'salon_info' in cus:
            if 'salon_cr_name' in  cus['salon_info']:
                print("change salon_cr_name" + cus['salon_info']['salon_cr_name'] + " to " + fullname)
                cus['salon_info']['salon_cr_name'] = fullname
        reg_items = cus['reg_items']
        for item in reg_items:
            if item['id'] == 'customer.fullname':
                print("change customer.fullname "+ item['value'] + " to " + fullname)
                item['value'] = fullname
            elif item['id'] == 'customer.fullnameKana':
                print("change customer.fullnameKana "+ item['value'] + " to " + fullnameKana)
                item['value'] = fullnameKana
            elif item['id'] == 'customer.gender':
                print("change customer.gender "+ item['value'] + " to "+ str(gender))
                item['value'] = int(gender)

        index+=1
    print(cus_json_data)
    with open(G_CUS_JSON_DATA_NEW,'w',encoding='utf-8') as nf:
        json.dump(cus_json_data,nf,indent=4,ensure_ascii=False)



