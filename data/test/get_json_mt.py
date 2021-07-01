'''Script to get json objects from xmrchain.net with multithreading'''
import requests
import json

#parsed at block 2112472, approx 03-06-2020 1952hrs
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

for i in range(2112472):    #monero block height starts at 0
    if i%10==0:
        print("Reached block {}".format(i))
    response = requests.get("http://xmrchain.net/api/block/{}".format(str(i)))
    block = json.loads(response.content)

    with open('blocks/{}.json'.format(i), 'w') as f:    #dump block data as json
        json.dump(block, f, indent=4)

    data = block["data"]
    txs=[]

    for tx in data["txs"]:
        txs.append(tx["tx_hash"])

    for hash in txs:
        response = requests.get("http://xmrchain.net/api/transaction/{}".format(hash))
        tx = json.loads(response.content)
        with open('txs/{}.json'.format(hash), 'w') as f:    #dump tx data as json
            json.dump(tx, f, indent=4)

tac()
