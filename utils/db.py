'''
A module for storing functions and other constants (if need be) for fetching data from our database:
'''

import os, sqlite3
from utils import funcs

def fetch_data(access_key, fernet_key):
    '''
    Given an access key and a Fernet key for decrypting the database, fetch and decrypt 
    the database's fields.  
    
    If the access and decryption are successful, return a list of dictionaries 
    containing the database's data; if not, return a dictionary object that contains the status code 
    and error message.
    '''
    try:
        if access_key != os.getenv('ACCESS_KEY'):
            return({'status' : 403, 'message' : 'incorrect / missing access key'})
        elif fernet_key != os.getenv('FERNET_KEY'):
            return({'status' : 403, 'message' : 'incorrect / missing fernet key'})
        conn = sqlite3.connect('./db/data.db') ; cursor = conn.cursor() ; cursor.execute('SELECT * FROM "Patient Information"')
        results, colnames = cursor.fetchall(), [i[0].lower() for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        results = [tuple(map(lambda x : funcs.decrypt(x, fernet_key), i)) for i in results] ; conn.close()
        return([dict(zip(colnames, i)) for i in results], 200)
    except (Exception, sqlite3.Error) as e:
        return({'status' : 500, 'message' : str(e)}, 500)