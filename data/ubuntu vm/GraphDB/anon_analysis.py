'''
Subsequent rounds of de-anonymization
'''
import subprocess
import os
import json
import csv
from arango import ArangoClient

with open("/home/VMadmin/data/progress.txt", "r") as text_file:
    start = int(text_file.readline())+1
text_file.close()


#Connect to db and load graph
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('monero', username='root', password='')
monero = db.graph('monero')

for i in range(start, 1980622):

    with open("/home/VMadmin/data/blocks/{}.json".format(i)) as json_file:
        dict = json.load(json_file)
    json_file.close()

    data = dict["data"]
    txs = data['txs']

    for tx in txs:
        hash = str(tx["tx_hash"])
        if tx["coinbase"] == True:
                pass
        else:

            ec = monero.edge_collection("input_of")
            ec1 = monero.edge_collection("ring_member_of")

            vc = monero.vertex_collection("ring_members")
            vc1 = monero.vertex_collection("inputs")
            vc2 = monero.vertex_collection("outputs")

            with open("/home/VMadmin/data/inputs_count.txt", "r") as text_file:
                inputs_count = int(text_file.readline())
            text_file.close()

            with open("/home/VMadmin/data/deanon_inputs.txt", "r") as text_file:
                deanon_inputs = int(text_file.readline())
            text_file.close()

            inputs = ec.edges("txs/{}".format(hash),"in")['edges']
            inputs = [str(input['_from']) for input in inputs]

            for input in inputs:

                input_json = vc1.get(input)
                inputs_count+=1

                if 'deanon' in input_json.keys() and input_json['deanon']==True:
                    deanon_inputs+=1
                else:

                    ring_members = ec1.edges(input, "in")['edges']
                    ring_members = [str(ring_member['_from']) for ring_member in ring_members]
                    unspent = []

                    for ring_member in ring_members:
                        pk_str = ring_member.split(',')[1]
                        pk_json = vc2.get(pk_str)
                        if not 'spent' in pk_json.keys() or pk_json['spent'] ==False:
                            unspent.append(ring_member)

                    unspent_count = len(unspent)

                    if unspent_count == 1:

                        deanon_inputs+=1
                        rm = vc.get(ring_members[0])
                        rm['true_input'] = True
                        vc.update(rm)

                        ip = vc1.get(input)
                        ip['deanon'] = True
                        vc1.update(ip)

                        pk = rm['pub_key']
                        op = vc2.get(pk)
                        op['spent'] = True
                        vc2.update(op)

            with open("/home/VMadmin/data/inputs_count.txt", "w") as text_file:
                text_file.write("{}".format(inputs_count))
            text_file.close()

            with open("/home/VMadmin/data/deanon_inputs.txt", "w") as text_file:
                text_file.write("{}".format(deanon_inputs))
            text_file.close()

    if i%1000==0 or i==1980622:
        with open("/home/VMadmin/data/inputs_count.txt", "r") as text_file:
            inputs_count = int(text_file.readline())
        text_file.close()

        with open("/home/VMadmin/data/deanon_inputs.txt", "r") as text_file:
            deanon_inputs = int(text_file.readline())
        text_file.close()

        deanon_ratio = float(deanon_inputs)/float(inputs_count)

        with open('/home/VMadmin/data/round2.csv', 'a') as file:
            csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([i, deanon_ratio])
        file.close()

    with open("/home/VMadmin/data/progress.txt", "w") as text_file:
        text_file.write("{}".format(i))
    text_file.close()
