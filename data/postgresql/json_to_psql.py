import psycopg2
import os
import json
import shutil
import glob

blocks = os.listdir("blocks")

for block in blocks:
    #get relevant data
    with open("blocks/{}".format(block), "r") as json_data:
      dict = json.loads(json_data.read())
    data = dict["data"]
    txs=[]
    for tx in data["txs"]:
        txs.append(tx["tx_hash"])
    blocks_row = [
    str(data["block_height"]),
    data["hash"],
    txs,
    data["timestamp_utc"]
    ]

    #write to blocks
    try:
        conn = psycopg2.connect(host="localhost",database="monero", user="postgres", password="")
        cur = conn.cursor()
        cur.execute("INSERT INTO blocks VALUES(%s, %s, %s, %s)", blocks_row)
        conn.commit()
        cur.close()
    except psycopg2.errors.UniqueViolation:
        print("attempted to write existing data")
    shutil.move("blocks/{}".format(block), "dumped_blocks/{}".format(block))

txs = glob.glob("txs/*/*.json")
for tx in txs:
    tx_hash = tx.split("\\")[2]
    with open(tx, "r") as json_data:
      dict = json.loads(json_data.read())
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
            inputs_rows.append([input["key_image"], input["amount"], mixin_no])
            key_img = input["key_image"]
            if input["mixins"]!=None:
                for mixin in input["mixins"]:
                    mixins_rows.append([key_img, mixin["public_key"], mixin["block_no"]])

    pk=[]
    outputs_rows = []

    if data["outputs"]!=None:
        for output in data["outputs"]:
            pk.append(output["public_key"])
            outputs_rows.append([output["public_key"], output["amount"]])

    txs_row = [
    data["tx_hash"],
    str(data["block_height"]),
    data["coinbase"],
    ki,
    pk
    ]

    #write to txs
    try:
        conn = psycopg2.connect(host="localhost",database="monero", user="postgres", password="HZ^p[6mbYvJ7NG^N")
        cur = conn.cursor()
        cur.execute("INSERT INTO txs VALUES(%s, %s, %s, %s, %s)", txs_row)
        conn.commit()
        cur.close()
    except psycopg2.errors.UniqueViolation:
        print("attempted to write existing data")

    #write to inputs
    for row in inputs_rows:
        try:
            conn = psycopg2.connect(host="localhost",database="monero", user="postgres", password="HZ^p[6mbYvJ7NG^N")
            cur = conn.cursor()
            cur.execute("INSERT INTO inputs VALUES(%s, %s, %s)", row)
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation:
            print("attempted to write existing data")

    #write to outputs
    for row in outputs_rows:
        try:
            conn = psycopg2.connect(host="localhost",database="monero", user="postgres", password="HZ^p[6mbYvJ7NG^N")
            cur = conn.cursor()
            cur.execute("INSERT INTO outputs VALUES(%s, %s)", row)
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation:
            print("attempted to write existing data")

    #write to mixins
    for row in mixins_rows:
        try:
            conn = psycopg2.connect(host="localhost",database="monero", user="postgres", password="HZ^p[6mbYvJ7NG^N")
            cur = conn.cursor()
            cur.execute("INSERT INTO mixins VALUES(%s, %s, %s)", row)
            conn.commit()
            cur.close()
        except psycopg2.errors.UniqueViolation:
            print("attempted to write existing data")

    shutil.move(tx, "dumped_txs/{}".format(tx_hash))
