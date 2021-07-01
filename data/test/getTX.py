'''Script to generate other tables from blocks tables'''
import requests
import json
import csv
import pandas as pd
import time
#test 1: 27 min 4 secs
_start_time = time.time()
def tic():
    global _start_time
    _start_time = time.time()

def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    print('Time passed: {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec))
tic()

blocks = pd.read_csv("blocks.csv", usecols=["txs"])
txs=[]
for item in blocks.txs:
    for hash in eval(item):
        txs.append(hash)

for hash in txs:
    response = requests.get("http://xmrchain.net/api/transaction/{}".format(hash))
    dict = json.loads(response.content)
    data = dict["data"]

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

    pk=[]
    outputs_rows = []
    if data["outputs"]!=None:
        for output in data["outputs"]:
            pk.append(output["public_key"])
            outputs_rows.append([output["public_key"], hash, output["amount"]])

    #writing to txs table
    txs_row = [
    data["tx_hash"],
    data["block_height"],
    data["coinbase"],
    ki,
    pk
    ]

    with open("txs.csv", mode='a') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(txs_row)
    file.close()

    #writing to inputs table
    for row in inputs_rows:
        with open("inputs.csv", mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
        file.close()

    #writing to outputs table
    for row in outputs_rows:
        with open("outputs.csv", mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
        file.close()

    #writing to mixins table
    for row in mixins_rows:
        with open("mixins.csv", mode='a') as file:
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)
        file.close()

tac()
