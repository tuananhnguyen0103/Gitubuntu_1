import pandas as pd
from flask import Flask, jsonify, request
import sql
import os
import mysql.connector 

app = Flask(__name__)

def get_data(date, unit_id, group_id, student_id,calo_range):
    
    
    df = sql.api_get_suggestion(date, unit_id, group_id, student_id,calo_range)
    
    json_data = df.to_json()

    return json_data
    
    

@app.route('/api/data', methods=['GET'])
def api_data():
    clear = lambda: os.system('cls')
    clear()
    date = request.form.get('date')
    unit_id = request.form.get('unit_id')
    group_id = request.form.get('group_id')
    student_id = request.form.get('student_id')
    calo_range = request.form.get('calo_range')
    json_data = get_data(date, unit_id, group_id, student_id,calo_range)
    return json_data
@app.route('/api/hello', methods=['GET'])
def hello():
    # Prepare the response
    response = {
        'message': 'Hello, how are you'
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
