import subprocess
import os
import json
from arango import ArangoClient
import arango
import csv

#Connect to db and load graph
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('monero', username='root', password='')
monero = db.graph('monero')

with open("progress.txt", 'r') as text_file:
    i = int(text_file.readline())+1
text_file.close()


#Extract json files from archive
extract_cmd = ["tar", "-zxf", "txs/{}.tar.gz".format(i)]
subprocess.call(extract_cmd)

#Handle missing json files
if not os.path.isdir("txs/{}".format(i)) or len(os.listdir("txs/{}".format(i)))==0:

    with open('missing_data_log.txt', 'a') as logfile:
        logfile.write('Missing files at block{}\n'.format(i))
    logfile.close()
    with open("missing_data.txt", "w") as file:
        file.write(str(i))
    file.close()
    re_get_cmd = ["python", "re_get_json.py"]
    subprocess.call(re_get_cmd)
    extract_cmd = ["tar", "-zxf", "txs/{}.tar.gz".format(i)]
    subprocess.call(extract_cmd)
    txs = os.listdir("txs/{}".format(i))
    if len(txs)>0:
        with open('missing_data_log.txt', 'a') as logfile:
            logfile.write('Successfully re-got json tx files\n')
        logfile.close()

txs = os.listdir("txs/{}".format(i))

for tx in txs:
    with open("txs/{}/{}".format(i,tx)) as json_file:
        dict = json.load(json_file)
    data = dict["data"]

    hash = data["tx_hash"]
    blk_height = data["block_height"]
    timestamp = data["timestamp"]

    if data["coinbase"] == True:
        try:
            monero.insert_vertex('cb_txs', {'_key': str(hash), 'hash': hash, 'blk_height': blk_height, 'timestamp': timestamp})
        except Exception as e:
            print(e)
    else:
        try:
            monero.insert_vertex('txs', {'_key': hash, 'hash':hash, 'blk_height': blk_height, 'timestamp': timestamp})
        except Exception as e:
            print(e)

    if data["outputs"]:
        for output in data["outputs"]:

            pub_key = output["public_key"]
            amt = output["amount"]
            outputs = monero.vertex_collection('outputs')

            #If pubkey already exists, add new edge with tx amount, and update total inputs.
            if outputs.has(str(pub_key)):

                existing_total_inputs = outputs.get(str(pub_key))['total_inputs']
                new_total_input = existing_total_inputs + amt

                if data["coinbase"] == True:
                    try:
                        monero.link('has_output', 'cb_txs/{}'.format(str(hash)), 'outputs/{}'.format(str(pub_key)), data = {'total_inputs': amt})
                    except Exception as e:
                        print(e)
                else:
                    try:
                        monero.link('has_output', 'txs/{}'.format(str(hash)), 'outputs/{}'.format(str(pub_key)), data = {'total_inputs': amt})
                    except Exception as e:
                        print(e)
                try:
                    outputs.update({'_key': str(pub_key), 'pub_key': pub_key, 'total_inputs': new_total_input})
                except Exception as e:
                    print(e)

            else:
                try:
                    outputs.insert({'_key': str(pub_key), 'pub_key': pub_key, 'total_inputs': amt})
                except Exception as e:
                    print(e)
                if data["coinbase"] == True:
                    try:
                        monero.link('has_output', 'cb_txs/{}'.format(str(hash)), 'outputs/{}'.format(str(pub_key)), data = {'total_inputs': amt})
                    except Exception as e:
                        print(e)
                else:
                    try:
                        monero.link('has_output', 'txs/{}'.format(str(hash)), 'outputs/{}'.format(str(pub_key)), data = {'total_inputs': amt})
                    except Exception as e:
                        print(e)

    else:
        with open('zero_output_txs.csv', 'a') as zo_file:
            csv_writer = csv.writer(zo_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([blk_height, hash])
        zo_file.close()

    if data["inputs"]:
        for input in data["inputs"]:
            ki = input["key_image"]
            amt = input["amount"]
            try:
                monero.insert_vertex('inputs', {'_key': str(ki), 'key_img': ki, 'tx_amt': amt})
            except Exception as e:
                print(e)
            try:
                monero.link('input_of', 'inputs/{}'.format(str(ki)), 'txs/{}'.format(str(hash)))
            except Exception as e:
                print(e)

            mixins = input["mixins"]
            pks = [mixin['public_key'] for mixin in mixins]

            for idx, mixin in enumerate(mixins):

                pk = mixin["public_key"]
                blk_height = mixin["block_no"]

                if pks.count(pk)>1:
                    duplicate = True
                else:
                    duplicate = False

                key = str(ki)+','+str(pk)+','+str(idx)
                try:
                    monero.insert_vertex('ring_members', {'_key': key, 'key_img': ki, 'pub_key': pk, 'idx': idx, 'blk_height': blk_height, 'duplicate': duplicate})
                except Exception as e:
                    print(e)
                try:
                    monero.link('ring_member_of', 'ring_members/{}'.format(key), 'inputs/{}'.format(ki))
                except Exception as e:
                    print(e)
                try:
                    monero.link('used_as', 'outputs/{}'.format(str(pk)), 'ring_members/{}'.format(key))
                except Exception as e:
                    print(e)

    json_file.close()


#Archive tx directories after dumping json files to save on inodes
zip_command = ["tar", "-zcf", "txs/{}.tar.gz".format(i), "txs/{}/".format(i)]
subprocess.call(zip_command)
rm_command = ["rm", "-r", "txs/{}".format(i)]
subprocess.call(rm_command)

with open("progress.txt", "w") as text_file:
    text_file.write("{}".format(i))
text_file.close()
