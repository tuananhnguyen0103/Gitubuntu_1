# import lib.functions as lib 


# # print(lib.calculate_BMI(50,170))
# # print(lib.interpret_BMI(lib.calculate_BMI(50,170)))

# import os
# import glob
# import joblib
# # Đường dẫn tới thư mục cha 2
# get_current_path = os.getcwd()
# parent_dir_2 = os.path.dirname(get_current_path)
# parent_dir_predict = os.path.join(parent_dir_2, "lib\\models_detect\\sex")
# files = os.listdir(parent_dir_predict)
# joblib_files = glob.glob(parent_dir_predict + '/*.joblib')
# # print(joblib_files)
# loaded_model = joblib.load(joblib_files[0])

# # Dự đoán giới tính của một câu nói
# text_to_predict = "Cô ấy là một người dễ thương và năng động."
# predicted_gender = loaded_model.predict([text_to_predict])
# print(predicted_gender)
# # # Đường dẫn tới thư mục 2.2
# # dir_2_2 = os.path.join(parent_dir_2, "2.2")

# # # Đường dẫn tới file bạn muốn lấy ở thư mục 2.2
# # file_in_2_2 = os.path.join(dir_2_2, "ten_file.txt")

# # # Kiểm tra xem file có tồn tại không
# # if os.path.exists(file_in_2_2):
# #     # Xử lý file ở đây
# #     print("File tồn tại:", file_in_2_2)
# # else:
# #     print("File không tồn tại:", file_in_2_2)