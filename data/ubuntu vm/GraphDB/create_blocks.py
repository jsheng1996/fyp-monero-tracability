from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://localhost:8529')

# Connect to "monero" database as root user.
db = client.db('monero', username='root', password='')
monero = db.graph('monero')

monero.create_vertex_collection('blocks')
monero.create_edge_definition(
        edge_collection='has_tx',
        from_vertex_collections=['blocks'],
        to_vertex_collections=['txs']
)

monero.create_edge_definition(
        edge_collection='has_cb_tx',
        from_vertex_collections=['blocks'],
        to_vertex_collections=['cb_txs']
)
print('Vertex collection "blocks" successfully created.')
