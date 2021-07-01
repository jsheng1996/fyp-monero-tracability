'''Script to generate txs table from blocks tables'''
import requests
import json
import csv
import pprint

response = requests.get("http://xmrchain.net/api/transaction/beb76a82ea17400cd6d7f595f70e1667d2018ed8f5a78d1ce07484222618c3cd")
dict = json.loads(response.content)
data = dict["data"]
#pprint.pprint(data)

ki=[]
inputs_rows = []
mixins_rows = []
if data["inputs"]!=None:
    for input in data["inputs"]:
        ki.append(input["key_image"])
        try:
            mixin_no = input["mixin"]
        except:
            mixin_no = len(input["mixins"])
        inputs_rows.append([input["key_image"], hash, input["amount"], mixin_no])
        key_img = input["key_image"]
        if input["mixins"]!=None:
            for mixin in input["mixins"]:
                mixins_rows.append([key_img, mixin["block_no"], mixin["public_key"]])
print(ki)
print(inputs_rows)
print(mixins_rows)
