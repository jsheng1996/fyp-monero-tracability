'''Script to get json objects from xmrchain.net'''
import requests
import json
import os
#parsed at block 2112472, approx 03-06-2020 1952hrs

for i in range(2112472):    #monero block height starts at 0
    if i%100==0:
        print("Reached block {}".format(i))
    response = requests.get("http://xmrchain.net/api/block/{}".format(str(i)))
    block = json.loads(response.content)

    with open('blocks/{}.json'.format(i), 'w') as f:    #dump block data as json
        json.dump(block, f, indent=4)

    data = block["data"]
    txs=[]

    os.makedirs("txs/{}".format(i), exist_ok=True)

    for tx in data["txs"]:
        txs.append(tx["tx_hash"])

    for hash in txs:
        response = requests.get("http://xmrchain.net/api/transaction/{}".format(hash))
        tx = json.loads(response.content)
        with open('txs/{}/{}.json'.format(i, hash), 'w') as f:    #dump tx data as json
            json.dump(tx, f, indent=4)
