'''
A Python file that contains routes for accessing and manipulating data within the database.
This file contains the code that was originally written in the main app.py file, albeit modularized 
to make things more readable.
'''

from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
from utils import db as db_funcs
import os, sqlitecloud

db = Blueprint('db', __name__)
load_dotenv()

@db.route('/fetch_information', methods = ['POST'])
def fetch_information():
    '''
    Tries to fetch information from the database provided that the access password has been given.  If not,
    return an error and do not return any data.
    '''
    data = request.get_json()
    results, code = db_funcs.fetch_data(data['access_key'], data['encryption_key'])
    return(jsonify(results), code)

@db.route('/post_information', methods = ['POST'])
def post_information():
    '''
    A route for uploading information onto the said database; it requires the access key, but not the 
    FERNET key for encrypting responses.
    '''
    try:
        data = request.get_json()
        if data.get('access_key') is None or data.get('access_key') != os.getenv('ACCESS_KEY'):
            return(jsonify({'status_code' : 403, 'message' : 'incorrect / missing access key'}), 403)
        conn = sqlitecloud.connect(os.getenv('CONNECTION_STRING')) 
        conn.execute('USE DATABASE lf_project_store') 
        cursor = conn.cursor() 
        colnames = [i[0] for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        enc_data = tuple([data[i] for i in colnames])
        cursor.execute(f'INSERT INTO "Patient Information" ({", ".join(colnames)}) VALUES ({", ".join(["?"] * len(enc_data))})', enc_data) 
        conn.commit() ; conn.close()
        return(jsonify({'status' : 200, 'message' : 'data successfully inserted'}), 200)
    except (Exception, sqlitecloud.Error) as e:
        return(jsonify({'status' : 500, 'message' : str(e)}), 500)
    
@db.route('/update_information', methods = ['PUT'])
def update_information():
    '''
    A route for updating information in the database.  Expects an access key
    to be supplied:
    '''
    try:
        data = request.get_json()
        if data.get('access_key') is None or data.get('access_key') != os.getenv('ACCESS_KEY'):
            return(jsonify({'status' : 403, 'message' : 'incorrect / missing access key'}), 403)
        elif len(data) <= 3:
            return(jsonify({'status' : 400, 'message' : 'too little parameters to update'}), 400)
        conn = sqlitecloud.connect(os.getenv('CONNECTION_STRING')) 
        conn.execute('USE DATABASE lf_project_store') 
        cursor = conn.cursor()
        colnames, values = [i for i in list(data.keys()) if i != 'access_key'], [str(i) for i in list(data.values())[1:]]
        data = dict(zip(colnames, values))

        # Find the appropriate ROWID here:
        cursor.execute('SELECT ROWID, patient_name, patient_nric FROM "Patient Information"') ; fetched = cursor.fetchall()
        row_ids, names, nrics = [list(map(lambda x : x[i], fetched)) for i in range(3)]
        row_id = list({i for i, v in enumerate(names) if v == data['patient_name']} & {i for i, v in enumerate(nrics) if v == data['patient_nric']})[0]
        
        # Do the updating here:
        to_update_keys = list(data.keys())[2:] ; to_update = [data[i] for i in to_update_keys]
        cursor.execute(f'UPDATE "Patient Information" SET {", ".join([f"{i} = ?" for i in to_update_keys])} WHERE ROWID = ?',
                       tuple(to_update + [row_ids[row_id]]))
        conn.commit() ; conn.close()
        return(jsonify({'status' : 200, 'message' : 'update successful'}), 200)
    except IndexError:
        return(jsonify({'status' : 400, 'message' : 'no such patient exists'}), 400)
    except KeyError:
        return(jsonify({'status' : 400, 'message' : 'a parameter is missing'}), 400)
    except (Exception, sqlitecloud.Error) as e:
        return(jsonify({'status' : 500, 'message' : str(e)}), 500)

@db.route('/delete_patient', methods = ['POST'])
def delete_patient():
    '''
    Given a patient's NRIC and Name, delete them from the database:
    '''
    try:
        data = request.get_json()
        if data.get('access_key') is None or data.get('access_key') != os.getenv('ACCESS_KEY'):
            return(jsonify({'status' : 403, 'message' : 'incorrect / missing access key'}), 403)
        elif len(data) > 3:
            return(jsonify({'status' : 400, 'message' : 'too many parameters to work with'}), 400)
        conn = sqlitecloud.connect(os.getenv('CONNECTION_STRING')) 
        conn.execute('USE DATABASE lf_project_store')
        cursor = conn.cursor()
        
        # Find the appropriate ROWID here:
        cursor.execute('SELECT ROWID, patient_name, patient_nric FROM "Patient Information"') ; fetched = cursor.fetchall()
        row_ids, names, nrics = [list(map(lambda x : x[i], fetched)) for i in range(3)]
        row_id = list({i for i, v in enumerate(names) if v == data['patient_name']} & {i for i, v in enumerate(nrics) if v == data['patient_nric']})[0]

        # Do the deletion here:
        cursor.execute('DELETE FROM "Patient Information" WHERE ROWID = ?', (row_ids[row_id], ))
        conn.commit() ; conn.close()
        return({'status' : 200, 'message' : 'patient successfully deleted'}, 200)
    except IndexError:
        return(jsonify({'status' : 400, 'message' : 'no such patient exists'}), 400)
    except KeyError:
        return(jsonify({'status' : 400, 'message' : 'incorrect / missing patient identifiers'}), 400)
    except (Exception, sqlitecloud.Error) as e:
        return(jsonify({'status' : 500, 'message' : str(e)}), 500)

@db.route('/delete_records', methods = ['DELETE'])
def delete_records():
    '''
    Clears the entire database (in case there's ever need to empty the cup out to speak of).
    '''
    data = request.get_json()
    if data.get('access_key') != os.getenv('ACCESS_KEY') and data.get('ENCRYPTION_KEY') != os.getenv('ENCRYPTION_KEY'):
        return(jsonify({'status' : 403, 'message' : 'incorrect / missing access key and / or encryption key.'}))
    try:
        conn = sqlitecloud.connect(os.getenv('CONNECTION_STRING')) 
        conn.execute('USE DATABASE lf_project_store')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM "Patient Information"')
        conn.commit() ; conn.close()
        return(jsonify({'status' : 200, 'message' : 'table successfully cleared'}))
    except (Exception, sqlitecloud.Error) as e:
        return(jsonify({'status' : 500, 'message' : e}))