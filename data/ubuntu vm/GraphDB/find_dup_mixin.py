import subprocess
import os
import json
import csv

for i in range(327625, 336254):
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

        if data["inputs"]:
            for input in data["inputs"]:

                ki = input["key_image"]
                mixins = input["mixins"]
                pks = [mixin['public_key'] for mixin in mixins]

                if len(pks) != len(set(pks)):

                    count = dict.fromkeys(set(pks), 0)
                    for pk in pks:
                        count[pk] += 1

                    for pk in list(set(pks)):
                        if count[pk]>1:
                            with open("dup_mixins.csv", 'a') as file:
                                csv_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                csv_writer.writerow([blk_height, hash, ki, count[pk]])
                            file.close()

#Archive tx directories after dumping json files to save on inodes
zip_command = ["tar", "-zcf", "txs/{}.tar.gz".format(i), "txs/{}/".format(i)]
subprocess.call(zip_command)
rm_command = ["rm", "-r", "txs/{}".format(i)]
subprocess.call(rm_command)
