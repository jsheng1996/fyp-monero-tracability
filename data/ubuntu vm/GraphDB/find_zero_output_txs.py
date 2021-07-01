import subprocess
import os
import json
import csv

for i in range(202612, 202613):
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

        if not data["outputs"]:

            with open('zero_output_txs.csv', 'a') as zo_file:
                csv_writer = csv.writer(zo_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                csv_writer.writerow([blk_height, hash])
            zo_file.close()
