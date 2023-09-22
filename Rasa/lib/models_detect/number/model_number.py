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

# Ví dụ với các dạng số khác nhau
height1 = "150cm"
height2 = "1m75"
height3 = "1.75m"
height4 = "1m6"

# Chuyển đổi và in kết quả
result1 = convert_height_to_meters(height1)
result2 = convert_height_to_meters(height2)
result3 = convert_height_to_meters(height3)
result4 = convert_height_to_meters(height4)

print(f"{height1} -> {result1} m")
print(f"{height2} -> {result2} m")
print(f"{height3} -> {result3} m")
print(f"{height4} -> {result4} m")


def calculate_BMI (weight, height):
    BMI = float(weight) / pow(float(height),2)
    BMI = round(BMI,2)
    return BMI

print(calculate_BMI(40.0,1.6))