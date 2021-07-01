import requests
import json
import csv

#parsed at block 2112472, approx 03-06-2020 1952hrs

#init
with open("blocks.csv", mode='r') as blocks:
    reader = csv.reader(blocks)
    rows = []
    for row in reader:
        rows.append(row)
    j = int(rows[-2][0])
    print(j)
blocks.close()

#read
for i in range(j+1,2112473):    #monero block height starts at 0
    if i%1000==0:
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
