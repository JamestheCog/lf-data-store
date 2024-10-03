'''
A module for storing functions and other constants (if need be) for fetching data from our database:
'''

import os, sqlitecloud

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
        conn = sqlitecloud.connect(os.getenv('CONNECTION_STRING')) ; conn.execute(f'USE DATABASE lf_project_store')
        cursor = conn.cursor() ; cursor.execute('SELECT * FROM "Patient Information"')
        results, colnames = cursor.fetchall(), [i[0].lower() for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        conn.close()
        return([dict(zip(colnames, i)) for i in results], 200)
    except (Exception, sqlitecloud.Error) as e:
        return({'status' : 500, 'message' : str(e)}, 500)