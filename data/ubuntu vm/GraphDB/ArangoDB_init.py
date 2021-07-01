from arango import ArangoClient

# Initialize the client for ArangoDB.
client = ArangoClient(hosts='http://localhost:8529')

# Connect to "_system" database as root user.
sys_db = client.db('_system', username='root', password='')

#Create database and graph
sys_db.create_database('monero')
db = client.db('monero', username='root', password='')
monero = db.create_graph('monero')

#Create vertex collections
monero.create_vertex_collection('cb_txs')
monero.create_vertex_collection('txs')
monero.create_vertex_collection('outputs')
monero.create_vertex_collection('inputs')
monero.create_vertex_collection('ring_members')

#Define edges
monero.create_edge_definition(
        edge_collection='has_output',
        from_vertex_collections=['cb_txs', 'tx'],
        to_vertex_collections=['outputs']
)

monero.create_edge_definition(
        edge_collection='input_of',
        from_vertex_collections=['inputs'],
        to_vertex_collections=['txs']
)

monero.create_edge_definition(
        edge_collection='ring_member_of',
        from_vertex_collections=['inputs'],
        to_vertex_collections=['ring_members']
)

monero.create_edge_definition(
        edge_collection='used_as',
        from_vertex_collections=['outputs'],
        to_vertex_collections=['ring_members']
)
