
def calculate_BMI (weight, height):
    BMI = float(weight) / pow(float(height),2)
    BMI = round(BMI,2)
    return BMI
def interpret_BMI(BMI):
    
    if BMI < 16:
        return "Gầy độ III"
    elif 16 <= BMI < 17:
        return "Gầy độ II"
    elif 17 <= BMI < 18.5:
        return "Gầy độ I"
    elif 18.5 <= BMI < 25:
        return "Bình thường"
    elif 25 <= BMI < 30:
        return "Thừa cân"
    elif 30 <= BMI < 35:
        return "Béo phì độ I"
    elif 35 <= BMI < 40:
        return "Béo phì độ II"
    elif BMI >= 40:
        return "Béo phì độ III"

def get_latest_value_gender(gender_list):
    for gender in reversed(gender_list):
        if gender != "không":
            return gender
    return None

import re

def convert_height_to_meters(height_str):
    # Tìm các phần số trong chuỗi
    numbers = re.findall(r'\d+\.\d+|\d+', height_str)
    
    # Nếu có số thập phân, chuyển về đơn vị số thập phân
    if len(numbers) > 1:
        decimal_number = float(numbers[0]) + float(numbers[1]) / 10 ** len(numbers[1])
    else:
        decimal_number = float(numbers[0])
    
    # Nếu đơn vị là cm, chuyển về m (meters)
    if "cm" in height_str.lower():
        decimal_number /= 100
    
    return decimal_number

def convert_weight_to_number(weight_str):
    # Loại bỏ các kí tự không phải số
    numbers = re.findall(r'\d+\.\d+|\d+', weight_str)
    
    # Tạo số từ chuỗi số đã loại bỏ kí tự
    if numbers:
        number = float("".join(numbers))
        return number
    else:
        return None