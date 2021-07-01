'''Script to get json objects from xmrchain.net'''
import requests
import json
import os
import datetime
from time import sleep
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import subprocess

#parsed at block 2112472, approx 03-06-2020 1952hrs

session = requests.Session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

print("Starting script at {}".format(datetime.datetime.now()))

for i in range(2112473):    #monero block height starts at 0
    response = session.get("https://xmrchain.net/api/block/{}".format(str(i)))
    block = json.loads(response.content)

    with open('blocks/{}.json'.format(i), 'w') as f:    #dump block data as json
        json.dump(block, f, indent=4)

    data = block["data"]
    txs=[]

    if not os.path.exists("txs/{}".format(i)):
        os.makedirs("txs/{}".format(i))

    for tx in data["txs"]:
        txs.append(tx["tx_hash"])

    for hash in txs:
        response = session.get("https://xmrchain.net/api/transaction/{}".format(hash))
        tx = json.loads(response.content)
        with open('txs/{}/{}.json'.format(i, hash), 'w') as f:    #dump tx data as json
            json.dump(tx, f, indent=4)

    #Archive tx directories after writing json files to save on inodes
    zip_command = ["tar", "-zcf", "txs/{}.tar.gz".format(i), "txs/{}/".format(i)]
    subprocess.call(zip_command)
    rm_command = ["rm", "-r", "txs/{}".format(i)]
    subprocess.call(rm_command)
