from arango import ArangoClient
import subprocess

#Drop db
client = ArangoClient(hosts='http://localhost:8529')
db = client.db('_system', username='root', password='')
db.delete_database('monero')

#Re-init db
init_cmd = ["python", "ArangoDB_init.py"]
subprocess.call(init_cmd)

#Reset counters
with open("data/progress.txt", "w") as
file:
    file.write("0")
file.close()
