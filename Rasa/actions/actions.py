
import feedparser

from typing import Any, Text, Dict, List
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import time 
import requests
import pandas as pd 
import lib.functions as lib 
import joblib
import os
import glob
kid_gender = []
### START FUCTION ###
def get_key_personal_conversation(tracker):
    key_converasation = tracker.latest_message["metadata"]["key"]
    return key_converasation

class GetTimeAction(Action):
    def name(self) -> Text:
        return "action_get_time"
    
    def run(self, dispatcher:  CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        current_time = datetime.now().strftime("%H:%M:%S")
        dispatcher.utter_message(text=f"Giờ hiện tại là:  {current_time}")
        # latest_message = tracker.latest_message
        
        # entities = tracker.current_state()
        # # Get the list of events from the conversation state
        # events = entities.get('events', [])
        # # text = events
        # # text = str(entity_values)
        # entity_values = []
        # for event in events:
        #     ##### KHÔNG API #####
        #     if event.get('event') == 'user':
        #         entities = event.get('parse_data', {}).get('entities', [])
        #     ##### KHÔNG API #####
        #     ##### CÓ API #####
        #     # if event.get('event') == 'user' and event.get('metadata')["key"]==key_converasation:
        #     #     entities = event.get('parse_data', {}).get('entities', [])
        #     ##### CÓ API #####
        #         for entity in entities:
        #             if entity['entity']=="user_name":
        #                 entity_values.append(entity.get('value'))

        # Lấy ra tất cả các value của slot mà mình lưu trong lịch sử chat và ghi vào trong file text.
        slot_names = tracker.slots.keys()
        
        # Tạo một dictionary để lưu trữ giá trị của các slot
        slot_values = {}
        
        # Lặp qua tên các slot và lấy giá trị từ tracker
        for slot_name in slot_names:
            slot_value = tracker.get_slot(slot_name)
            slot_values[slot_name] = slot_value
        
        # Trả về câu trả lời chứa giá trị của các slot
        response = "Các giá trị trong các slot là:\n"
        for slot_name, slot_value in slot_values.items():
            response += f"{slot_name}: {slot_value}\n"
        
        # Đường dẫn tới tệp cần ghi
        file_path = 'sample.txt'
        text = str(response)
        # Mở tệp để ghi
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

        # print("Chuỗi đã được ghi vào tệp", file_path)


        # Get the user's input sentence
        # user_sentence = latest_message['text']
                
        # get_current_path = os.getcwd()
        # parent_dir_2 = os.path.dirname(get_current_path)
        # parent_dir_predict = os.path.join(parent_dir_2, "Rasa\lib\models_detect\sex")
        # files = os.listdir(parent_dir_predict)
        # joblib_files = glob.glob(parent_dir_predict + '/*.joblib')
        # # print(joblib_files)
        # loaded_model = joblib.load(joblib_files[0])

        # # Dự đoán giới tính của một câu nói
        # text_to_predict = "Con gái, cân nặng 18kg và chiều cao 1.08m."
        # predicted_gender = loaded_model.predict([user_sentence])
        # # Câu nói bạn muốn dự đoán độ tự tin
        # new_text = "Cậu ấy là một người rất tài năng và sáng tạo."

        # # Dự đoán nhãn và độ tự tin
        # predicted_prob = loaded_model.predict_proba([new_text])

        # # Lấy độ tự tin cho mỗi nhãn
        # confidence_male = predicted_prob[0][loaded_model.classes_ == "nam"]
        # confidence_female = predicted_prob[0][loaded_model.classes_ == "nữ"]

        # print("Độ tự tin phân loại nam:", confidence_male)
        # print("Độ tự tin phân loại nữ:", confidence_female)
        # # print(predicted_gender)
        # dispatcher.utter_message(text=f"Giờ hiện tại là:  {confidence_male}")
        # dispatcher.utter_message(text=f"Giờ hiện tại là:  {confidence_female}")
        return []



class ActionGreet(Action):
    def name(self) -> Text:
        return "action_greet_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # key_converasation = get_key_personal_conversation(tracker)
        # entities = tracker.events
        entities = tracker.current_state()
        # Get the list of events from the conversation state
        events = entities.get('events', [])
        entity_values = []
        for event in events:
            ##### KHÔNG API #####
            if event.get('event') == 'user':
                entities = event.get('parse_data', {}).get('entities', [])
            ##### KHÔNG API #####
            ##### CÓ API #####
            # if event.get('event') == 'user' and event.get('metadata')["key"]==key_converasation:
            #     entities = event.get('parse_data', {}).get('entities', [])
            ##### CÓ API #####
                for entity in entities:
                    if entity['entity']=="user_name":
                        entity_values.append(entity.get('value'))
        # dispatcher.utter_message(text=f"Giờ hiện tại là:{entity_values}")
        user_name_entity = entity_values[-1]
        user_name = user_name_entity if user_name_entity else "khách"
        dispatcher.utter_message(response="utter_greet_name", user_name=user_name)
        return [SlotSet("user_name", user_name)]


#%% Story user describing obesity kid - Bot repply with info of user providing of kid
class ActionKidObesity(Action):
    def name(self) -> Text:
        return "action_repply_kid_obesity"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # key_converasation = get_key_personal_conversation(tracker)
        # entities = tracker.events
        entities = tracker.current_state()
        # Get the list of events from the conversation state
        events = entities.get('events', [])
        # entity_values = []
        user_kid = []
        kid_kg_weight = []
        kid_cm_height = []
        kid_m_height = []
        

        latest_message = tracker.latest_message

        # Get the user's input sentence
        user_sentence = latest_message['text']
                
        get_current_path = os.getcwd()
        parent_dir_2 = os.path.dirname(get_current_path)
        parent_dir_predict = os.path.join(parent_dir_2, "Rasa\lib\models_detect\sex")
        # files = os.listdir(parent_dir_predict)
        joblib_files = glob.glob(parent_dir_predict + '/*.joblib')
        # print(joblib_files)
        loaded_model = joblib.load(joblib_files[0])
        predicted_prob = loaded_model.predict_proba([user_sentence])

        # Lấy độ tự tin cho mỗi nhãn
        confidence_male = predicted_prob[0][loaded_model.classes_ == "nam"]
        confidence_female = predicted_prob[0][loaded_model.classes_ == "nữ"]
        
        gender = "không"
        if confidence_male >= 0.75:
            gender = "nam"
            kid_gender.append("nam")
        elif confidence_female >= 0.75:
            gender = "nữ"
            kid_gender.append("nữ")
        else:
            kid_gender.append("không")
        # kid_gender = kid_gender.append(gender)
        
        # dispatcher.utter_message(text=f"Giờ hiện tại là:{confidence_female} {confidence_male}")
        for event in events:
            ##### KHÔNG API #####
            if event.get('event') == 'user':
                entities = event.get('parse_data', {}).get('entities', [])
            ##### KHÔNG API #####
            ##### CÓ API #####
            # if event.get('event') == 'user' and event.get('metadata')["key"]==key_converasation:
            #     entities = event.get('parse_data', {}).get('entities', [])
            ##### CÓ API #####
                for entity in entities:
                    if entity['entity']=="user_kid":
                        user_kid.append(entity.get('value'))
                    if entity['entity']=="kid_kg_weight":
                        kid_kg_weight.append(entity.get('value'))
                    # if entity['entity']==" ":
                    #     kid_cm_height.append(entity.get('value'))
                    if entity['entity']=="kid_m_height":
                        kid_m_height.append(entity.get('value'))
                    
        result_gender = lib.get_latest_value_gender(kid_gender)
        entity_values = {
            "user_kid": user_kid,
            "kid_kg_weight": kid_kg_weight,
            "kid_m_height" : kid_m_height,
            "kid_cm_height" : kid_cm_height,
            "kid_gender_list" : kid_gender,
            "kid_gender": result_gender
        }
        
        if( result_gender == None and 
            len(entity_values['kid_m_height'])== 0 and 
                len(entity_values['kid_kg_weight']) == 0):
                    dispatcher.utter_message(response="utter_require_kid_height_weight_gender")
        elif(len(entity_values['kid_m_height'])== 0 and 
            len(entity_values['kid_kg_weight']) == 0):
                dispatcher.utter_message(response="utter_require_kid_height_weight")
        elif(result_gender == None and 
            len(entity_values['kid_kg_weight']) == 0):
                dispatcher.utter_message(response="utter_require_kid_weight_gender")
        elif(result_gender == None and 
            len(entity_values['kid_m_height'])== 0):
            dispatcher.utter_message(response="utter_require_kid_height_gender")
        elif(result_gender == None) :
            dispatcher.utter_message(response="utter_require_kid_gender")
        elif(len(entity_values['kid_kg_weight']) == 0):
            dispatcher.utter_message(response="utter_require_kid_weight")
        elif(len(entity_values['kid_m_height']) == 0) :
            dispatcher.utter_message(response="utter_require_kid_height")
        else:
            dispatcher.utter_message(response="utter_confirm_id_infor",kid_gender=result_gender,kid_m_height = kid_m_height[-1],kid_kg_weight=kid_kg_weight[-1])
            return [SlotSet("kid_gender", result_gender),SlotSet("kid_m_height", kid_m_height) ,SlotSet("kid_kg_weight", kid_kg_weight) ,SlotSet("user_kid", user_kid)] 
            
       
        # # text = events
        # text = str(entity_values)

        # # Đường dẫn tới tệp cần ghi
        # file_path = 'sample.txt'

        # # Mở tệp để ghi
        # with open(file_path, 'w', encoding='utf-8') as file:
        #     file.write(text)

        # print("Chuỗi đã được ghi vào tệp", file_path)

        # dispatcher.utter_message(text=f"Giờ hiện tại là:{entity_values}")
        # user_name_entity = entity_values[-1]
        # user_name = user_name_entity if user_name_entity else "khách"
        # dispatcher.utter_message(response="utter_greet_name", user_name=user_name)
        return 
        # [SlotSet("kid_gender", result_gender)]
        # , [SlotSet("kid_gender", result_gender)], [SlotSet("user_kid", user_kid)], [SlotSet("kid_kg_weight", kid_kg_weight)], [SlotSet("kid_m_height", kid_m_height)] 

class ActionBMI(Action):
    def name(self) -> Text:
        return "action_kid_BMI"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # key_converasation = get_key_personal_conversation(tracker)
        # entities = tracker.events
        entities = tracker.current_state()
        # Get the list of events from the conversation state
        events = entities.get('events', [])
        entity_values = []
        kid_kg_weight = []
        kid_cm_height = []
        kid_m_height = []
        result_gender = lib.get_latest_value_gender(kid_gender)
        
        for event in events:
            ##### KHÔNG API #####
            if event.get('event') == 'user':
                entities = event.get('parse_data', {}).get('entities', [])
            ##### KHÔNG API #####
            ##### CÓ API #####
            # if event.get('event') == 'user' and event.get('metadata')["key"]==key_converasation:
            #     entities = event.get('parse_data', {}).get('entities', [])
            ##### CÓ API #####
                for entity in entities:
                    if entity['entity']=="kid_kg_weight":
                        kid_kg_weight.append(entity.get('value'))
                    if entity['entity']=="kid_cm_height":
                        kid_cm_height.append(entity.get('value'))
                    if entity['entity']=="kid_m_height":
                        kid_m_height.append(entity.get('value'))
        entity_values = {
            "kid_kg_weight": lib.convert_weight_to_number(kid_kg_weight[-1]),
            "kid_m_height" : lib.convert_height_to_meters(kid_m_height[-1]),
            # "kid_cm_height" : lib.convert_height_to_meters(kid_cm_height[-1]),
            "kid_gender_list" : kid_gender,
            "kid_gender": result_gender
        }
        calculate_kid_kg_weight= float(lib.convert_weight_to_number(kid_kg_weight[-1]))
        calculate_kid_m_height = float(lib.convert_height_to_meters(kid_m_height[-1]))
        print(calculate_kid_kg_weight)
        print(calculate_kid_m_height)

        BMI = lib.calculate_BMI(calculate_kid_kg_weight,calculate_kid_m_height)      

        print(type(BMI))

        dispatcher.utter_message(text=f"Dựa vào thông tin mà bạn cung cấp. thì cháu có chỉ số BMI là {BMI} và cháu thuộc dạng {lib.interpret_BMI(BMI)}")
        if BMI < 16.0:
            dispatcher.utter_message(response="utter_under_weight_grade_I")
        elif 16.0 <= BMI < 17.0:
            dispatcher.utter_message(response="utter_under_weight_grade_II")
        elif 17.0 <= BMI < 18.5:
            dispatcher.utter_message(response="utter_under_weight_grade_III")
        elif 18.5 <= BMI < 25.0:
            dispatcher.utter_message(response="utter_normal_weight")
        elif 25.0 <= BMI < 30.0:
            dispatcher.utter_message(response="utter_over_weight")
        elif 30.0 <= BMI < 35.0:
            dispatcher.utter_message(response="utter_over_weight_grade_I")
        elif 35.0 <= BMI < 40.0:
            dispatcher.utter_message(response="utter_over_weight_grade_II")
        elif BMI >= 40.0:
            dispatcher.utter_message(response="utter_over_weight_grade_III")
        
        # return []
class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_fallback"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message("Tôi không hiểu bạn đang nói gì, vui lòng diễn đạt rõ hơn.")


