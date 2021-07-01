import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Connect to PostgreSQL DB
con = psycopg2.connect(dbname='postgres',
      user='postgres', host='localhost',
      password='')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# Obtain a DB Cursor
cursor = con.cursor()

#Create db 'monero'
cursor.execute("create database monero;")
con.close()

con = psycopg2.connect(dbname='monero',
      user='postgres', host='localhost',
      password='')
con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = con.cursor()

create_blocks = '''CREATE TABLE blocks (
height INTEGER PRIMARY KEY,
blk_hash CHAR(64),
txs CHAR(64) [],
timestamp TIMESTAMP);'''
cursor.execute(create_blocks)

create_txs = '''CREATE TABLE txs (
tx_hash CHAR(64) PRIMARY KEY,
blk_height INTEGER,
cb_tx BOOL,
input_KIs CHAR(64) [],
output_pubkeys CHAR(64) []);'''
cursor.execute(create_txs)

create_inputs = '''CREATE TABLE inputs (
tx_hash CHAR(64) PRIMARY KEY,
tx_amt VARCHAR,
mixin SMALLINT);'''
cursor.execute(create_inputs)

create_outputs = '''CREATE TABLE outputs (
tx_hash CHAR(64) PRIMARY KEY,
tx_amt VARCHAR);'''
cursor.execute(create_outputs)

create_mixins = '''CREATE TABLE mixins (
key_img CHAR(64),
output_pubkey CHAR(64),
pubkey_blk_height INTEGER,
PRIMARY KEY (key_img,output_pubkey));'''
cursor.execute(create_mixins)

con.close()
