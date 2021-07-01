'''Script to generate blocks table from xmrchain.net'''
import requests
import json
import csv
import time
#test 1: 26 min 51 secs
_start_time = time.time()
def tic():
    global _start_time
    _start_time = time.time()

def tac():
    t_sec = round(time.time() - _start_time)
    (t_min, t_sec) = divmod(t_sec,60)
    (t_hour,t_min) = divmod(t_min,60)
    print('Time passed: {}hour:{}min:{}sec'.format(t_hour,t_min,t_sec))

#parsed at block 2112472, approx 03-06-2020 1952hrs
tic()

for i in range(1000):    #monero block height starts at 0
    if i%10==0:
        print("Reached block {}".format(i))
    response =requests.get("http://xmrchain.net/api/block/{}".format(str(i)))
    dict = json.loads(response.content)
    data = dict["data"]
    txs=[]
    for tx in data["txs"]:
        txs.append(tx["tx_hash"])
    row = [
    data["block_height"],
    data["hash"],
    txs,
    data["timestamp_utc"]
    ]

    with open("blocks.csv", mode='a') as blocks:
        writer = csv.writer(blocks, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(row)
    blocks.close()

tac()
