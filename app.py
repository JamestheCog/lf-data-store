from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os, sqlite3, base64

# User modules:
from utils import funcs 

## Application start
app = Flask(__name__) ; load_dotenv()

@app.route('/post_information', methods = ['POST'])
def post_information():
    '''  
    Given a JSON object, post information onto the Firebase database:
    '''
    try:
        data = request.get_json() 
        if data['password'] != os.getenv('DB_PASSWORD') or data.get('password') is None:
            return(jsonify({'error' : 'bad password; did you key it in correctly?'}))
        data['patient_name'], data['patient_nric'], data['proxy_name'] = [funcs.encrypt(data[i], os.getenv('FERNET_KEY')) for i in ['patient_name', 'patient_nric', 'proxy_name']]

        # Insert the data here:
        conn = sqlite3.connect('./db/data.db') ; cursor = conn.cursor()
        column_names = [i[0] for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        cursor.execute(f'INSERT INTO "Patient Information" ({", ".join(column_names)}) VALUES ({", ".join(["?"] * len(column_names))})',
                       tuple([data[i] for i in column_names]))
        conn.commit() ; conn.close()
        return(jsonify({'status' : 200}), 200)
    except Exception as e:
        return(jsonify({'error' : str(e)}), 400)

@app.route('/get_information', methods = ['GET'])
def get_information():
    try:
        data = request.get_json() 
        if data['password'] != os.getenv('DB_PASSWORD') or data.get('password') is None:
            return({'error' : 'bad password; did you key it in correctly?'})
        conn = sqlite3.connect('./db/data.db') ; cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Patient Information"')
        retrieved_data, column_names = cursor.fetchall(), [i[0] for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        retrieved_data = [dict(zip(tuple(column_names), i)) for i in retrieved_data]
        for i in retrieved_data:
            i['patient_name'], i['patient_nric'], i['proxy_name'] = [funcs.decrypt(i[j], os.getenv('FERNET_KEY')) for j in ['patient_name', 'patient_nric', 'proxy_name']]
        conn.close() ; return(jsonify(retrieved_data), 200)
    except Exception as e:
        return(jsonify({'error' : str(e)}), 500)
    except sqlite3.Error as e:
        print(str(e))

@app.route('/update_information', methods = ['PATCH'])
def update_information():
    try:
        data = request.get_json() 
        if data['password'] != os.getenv('DB_PASSWORD') or data.get('password') is None:
            return({'error' : 'bad password; did you key it in correctly?'})
        conn = sqlite3.connect('./db/data.db') ; cursor = conn.cursor()
        column_names = [i[0] for i in cursor.execute('SELECT * FROM "Patient Information" LIMIT 1').description]
        data = dict(zip(column_names, list(request.get_json().values())))
        cursor.execute(f'UPDATE "Patient Information" SET {", ".join([i + " = " + data[i] for i in list(data.keys())[3:]])} WHERE {", ".join([i + " = " + data[i] for i in list(data.keys())[:3]])}')
        cursor.commit() ; conn.close()
        return(jsonify({'status' : 200}), 200)
    except Exception as e:
        return(jsonify({'error' : str(e)})), 400