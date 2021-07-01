from arango import ArangoClient

client = ArangoClient(hosts='http://localhost:8529')
db = client.db('monero', username='root', password='')
monero = db.graph('monero')
print('ok')
