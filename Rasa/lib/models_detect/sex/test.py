# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.pipeline import make_pipeline
# import numpy as np

# # Dữ liệu huấn luyện
# training_data = [
#     ("Cậu ấy là một người đàn ông lịch lãm và thông minh.", "nam"),
#     ("Cô ấy là một cô gái rất dễ thương và hoạt bát.", "nữ"),
#     ("Người đó có một vẻ ngoài nữ tính và dễ thương.", "nữ"),
#     ("Anh ta luôn chăm chỉ và nhiệt tình trong công việc.", "nam"),
#     ("Người đó thường ẩn dưới một tấm áo trùm.", "không"),
#     # Thêm các câu mô tả khác
# ]

# # Tách dữ liệu thành các câu nói và nhãn
# texts, labels = zip(*training_data)

# # Tạo model và train
# model = make_pipeline(CountVectorizer(), MultinomialNB())
# model.fit(texts, labels)

# # Dữ liệu kiểm tra
# test_data = [
#     "Người đó thường đi bộ một mình.",
#     "Cậu ấy thích chơi bóng đá.",
#     "Cô ấy làm việc chăm chỉ.",
#     "Người đó thường mặc váy và trang điểm.",
#     "Anh ta thích xem bóng rổ."
# ]
Code cmd 

# # Dự đoán giới tính cho dữ liệu kiểm tra
# predicted_labels = model.predict(test_data)

# # Dự đoán độ tự tin của mô hình cho dữ liệu kiểm tra
# confidence_scores = np.max(model.predict_proba(test_data), axis=1)

# # In kết quả
# for i in range(len(test_data)):
#     print(f"Đoạn văn: {test_data[i]}")
#     print(f"Dự đoán giới tính: {predicted_labels[i]}")
#     print(f"Độ tự tin: {confidence_scores[i]:.2f}\n")


list = []
list.append("hay")
obj = {
    "obj":list
}
print(obj)

