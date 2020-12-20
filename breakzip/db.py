import sqlite3
from sqlite3 import Error, OperationalError
import logging
logging.basicConfig(filename='breakzip.log', format='%(asctime)s %(message)s', level=logging.DEBUG)

def create_connection(db_name="file_sigs.db"):
    try:
        conn = sqlite3.connect(db_name)
    except Error as e:
        logging.error(e)
        raise e
    return conn

def init_db(conn):
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_signature
            (id INTEGER NOT NULL PRIMARY KEY, signature TEXT NOT NULL, file_type TEXT ) ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS file_extension
            (id INTEGER NOT NULL PRIMARY KEY, extension TEXT NOT NULL, file_signature_id INTEGER,
            FOREIGN KEY(file_signature_id) REFERENCES file_signatures(id))''')
    try:
        cursor.execute('''
            INSERT INTO file_signature VALUES(1, ?, "pkzip")''', (b"PK\x03\x04",))
        cursor.execute('''
            INSERT INTO file_signature VALUES(2, ?, "asf")''', (b"\x30\x26\xb2",))
        cursor.execute('''
            INSERT INTO file_signature VALUES(3, ?, "jpeg")''', (b"\xff\xd8",))
        cursor.execute('''
            INSERT INTO file_signature VALUES(4, ?, "png")''', (b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a",))
        cursor.execute('''
            INSERT INTO file_signature VALUES(5, ?, "xml")''', (b"\x3c\x3f\x78\x6d\x6c\x20",))
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("zip", 1)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("asf", 2)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("wmv", 2)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("wma", 2)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("jpg", 3)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("jpeg", 3)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("png", 4)''')
        cursor.execute('''
            INSERT INTO file_extension(extension, file_signature_id) VALUES("xml", 5)''')
    except sqlite3.IntegrityError as e:
        logging.warning(f"Rows already existed: {e}")
    except (Error, OperationalError) as e:
        logging.error(f'Something went wrong initializing DB. Rolling back: {e}')
        conn.rollback()
        raise e
    conn.commit()

def find_signature(conn, file_ext):
    cursor = conn.cursor()
    try:
        rows = cursor.execute('''
            SELECT signature FROM file_signature 
            INNER JOIN file_extension ON file_extension.file_signature_id = file_signature.id 
            WHERE extension = ?''', (file_ext,),).fetchall()
    except (Error, OperationalError) as e:
        logging.error(f'Something went wrong with the query: {e}')
    if rows and len(rows) >= 1:
        return rows[0][0]