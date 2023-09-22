# import test_firebase as FB
from flask import Flask, request, jsonify
from flask import Flask
from flask_socketio import SocketIO

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import firebase
import threading
import requests
import time
from datetime import datetime ,date
import pandas as pd
from flask import Flask, jsonify, request
import sql
import os
import mysql.connector 
app = Flask(__name__)
socketio = SocketIO(app)

#%% ---------------- FIREBASE --------------------------------

cred = credentials.Certificate('ura_key.json')
# # Get a reference to the root of your database
firebase_db = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ura-v2-default-rtdb.asia-southeast1.firebasedatabase.app/'
})
ref = db.reference('')
data = ref.get()

data_result = ""

# Function to handle the database changes
def handle_event(event):
    key = ""
    
    print(dir(event))
    try:
        key = event.path.split('/')[2]
        path_update = "messages/"+key+"/"
        print(event.path)
        print(key)
        print(path_update)
        print('Database changed:', event.event_type)
        print('Name user :', event.data["user"]["name"]) 
        if("botuser"== event.data["user"]["name"].lower()):
            data = {
                key: key,
            }
            time.sleep(2)
            url = "https://stg.ura.edu.vn/api/v1/bot/" +key +"/messages"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()  # Assuming the response is in JSON format
                value = data["data"][0]["content"]  # Replace "key" with the actual key in the response
                print(value)
            else:
                print("Error: Failed to retrieve data from the URL")

            API_ENDPOINT = "http://localhost:5005/webhooks/rest/webhook"

            # Define the input message
            message = value
            

            # Create the payload
            metadata = {
                "sender": "default",
                "message": message,
                "metadata": {
                    "key": key
                    }
            }

            # Send a POST request to the Rasa server
            response = requests.post(url=API_ENDPOINT, json=metadata)

            # Get the response from the Rasa server
            response_data = response.json()

            # Process the response
           
            context_bot =  ""
            for item in response_data:
                context_bot += item["text"] + "\n"
            print(context_bot)
            print("Leng: "+str(len(response_data)))
            print("Chatbot trả lời: " + str(response_data[0]["text"]))
            print("Data: " + str(response_data))
            data_push_firebase = {
                "createAt": datetime.now().timestamp(),
                "updateAt": datetime.now().timestamp(),
                "user": {
                    "_id": 0,
                    "name" : "botVietec"
                }
            }
            # db.reference('messages/'+str(key)).push(data_push_firebase)    
            print(data_push_firebase)
            

                        # API endpoint URL
            url_post =  "https://stg.ura.edu.vn/api/v1/bot/" +key +"/messages"
            # https://stg.ura.edu.vn/api/v1/bot/search?key=info&phone_number=0972806469 &conversation_id=694

            # Request payload
            payload = {
                'content': context_bot,
                # 'content': str(response_data[0]["text"]),
            }

            # Send POST request
            response = requests.post(url_post, json=payload)

            # Check response status code
            if response.status_code == 200 or response.status_code == 201 :
                # Request successful
                data = response.json()
                print('Response:', data)
                child_ref = ref.child(path_update)
                # child_ref = ref.child('messages')
                # print(dir(child_ref))
                # print("Nó chạy")
                child_ref.push().set(data_push_firebase)

            else:
                # Request failed
                print('Request failed with status code:', response.status_code)
    except:
        print('Database changed:', event.event_type)
        print('Data:', event.data)


    


# Function to listen for database changes in a separate thread
def listen_for_changes():
    
    event_stream = ref.listen(handle_event)

# Start listening for database changes in a separate thread
change_thread = threading.Thread(target=listen_for_changes)
change_thread.start()

#%%--------------------------- NLP----------------------------------------#

#%%--------------------------API------------------------------------------#

@app.route('/api/getvalue', methods=['POST'])
def your_api_endpoint():
    # Access the data sent to the API
    # data = request.json

    # Process the data (e.g., pass it to your Rasa model)

    # Prepare the response
    response = {
        'message': 'Your response message'
    }

    # Return the response as JSON
    return jsonify(response)

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
    
    # app.run(host='0.0.0.0', port=8686)
    # stream = ref.stream(handle_stream)
    socketio.run(app,host='0.0.0.0', port=8686)
    # print(123)
    # listen_for_changes()

if __name__ == '__main__':

    app.run(debug=True)
