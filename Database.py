import sqlite3
import os
from uuid import getnode as get_mac
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import getpass

def create_table(conn):
    # Create devices table with mac_address, name, private_key, and public_key columns
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            mac_address TEXT PRIMARY KEY,
            name TEXT,
            private_key BLOB,
            public_key BLOB
        )
    ''')
    conn.commit()

def insert_to_db(private_pem, public_pem, mac_address, db_filename="rsa_keys.db"):
    # Insert or update device keys in database
    username = getpass.getuser()

    if not os.path.exists(db_filename):
        conn = sqlite3.connect(db_filename)
        create_table(conn)
    else:
        conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO devices (mac_address, name, private_key, public_key)
        VALUES (?, ?, ?, ?)
    ''', (mac_address, username, private_pem, public_pem))

    conn.commit()
    conn.close()

def load_public_key_from_db(mac_address, db_filename="rsa_keys.db"):
    # Get public key from database by MAC address
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT public_key FROM devices WHERE mac_address=?", (mac_address,))
    result = cursor.fetchone()
    conn.close()
    if result:
        public_pem = result[0]
        return public_pem
    return None

def load_private_key_from_db(mac_address, db_filename="rsa_keys.db"):
    # Get private key from database by MAC address
    conn = sqlite3.connect(db_filename)
    cursor = conn.cursor()
    cursor.execute("SELECT private_key FROM devices WHERE mac_address=?", (mac_address,))
    result = cursor.fetchone()
    conn.close()
    if result:
        private_pem = result[0]
        return private_pem
    return None

