import pandas as pd
students = [
    {'id': 2470162, 'first_name': 'Nguyễn Văn', 'last_name': 'B', 'full_name': 'Nguyễn Văn B', 'age': 4, 'relation_id': 383, 'relationship': 'Mom', 'active': True, 'dob': '2019-11-01', 'gender': 'Nam', 'avatar': 'https://s3-hcm1-r1.longvan.net/uraapp/1611/conversions/IMG_0016-thumbnail.jpg', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484975, 'first_name': 'Nguyen Van', 'last_name': 'D', 'full_name': 'Nguyen Van D', 'age': 5, 'relation_id': 571, 'relationship': None, 'active': True, 'dob': '2018-01-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484976, 'first_name': 'Nguyen Van', 'last_name': 'E', 'full_name': 'Nguyen Van E', 'age': 5, 'relation_id': 579, 'relationship': None, 'active': True, 'dob': '2018-01-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484977, 'first_name': 'Nguyen Van', 'last_name': 'G', 'full_name': 'Nguyen Van G', 'age': 5, 'relation_id': 572, 'relationship': None, 'active': True, 'dob': '2018-01-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484978, 'first_name': 'Nguyen Van', 'last_name': 'H', 'full_name': 'Nguyen Van H', 'age': 5, 'relation_id': 577, 'relationship': None, 'active': True, 'dob': '2018-01-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']},
    {'id': 2484979, 'first_name': 'Nguyen Van', 'last_name': 'K', 'full_name': 'Nguyen Van K', 'age': 5, 'relation_id': 573, 'relationship': None, 'active': True, 'dob': '2018-02-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484980, 'first_name': 'Nguyen Van', 'last_name': 'M', 'full_name': 'Nguyen Van M', 'age': 5, 'relation_id': 578, 'relationship': None, 'active': True, 'dob': '2018-02-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484981, 'first_name': 'Nguyen Van', 'last_name': 'N', 'full_name': 'Nguyen Van N', 'age': 1005, 'relation_id': 576, 'relationship': None, 'active': True, 'dob': '1018-03-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']},
    {'id': 2484982, 'first_name': 'Nguyen Van', 'last_name': 'Q', 'full_name': 'Nguyen Van Q', 'age': 5, 'relation_id': 575, 'relationship': None, 'active': True, 'dob': '2018-03-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}, 
    {'id': 2484983, 'first_name': 'Nguyen Van', 'last_name': 'T', 'full_name': 'Nguyen Van T', 'age': 5, 'relation_id': 574, 'relationship': None, 'active': True, 'dob': '2018-04-01', 'gender': 'Nam', 'avatar': 'https://stg.ura.edu.vn/images/users/avatar_student_boy.png', 'address': '', 'block_age_name': 'Mẫu giáo lớn 5-6 tuổi', 'block_age_id': 6, 'blood_group': None, 'allergy': None, 'last_sick': None, 'height': None, 'weight': None, 'course_id': 66621, 'course_name': 'Lớp A3', 'school_name': 'Trường MN Training URA', 'visible_fee': None, 'is_ended': None, 'unit_settings': ['post.review', 'data.menu', 'data.plan', 'features.rate_sticker', 'features.checkin_checkout', 'features.chat', 'features.is_payment_gate_on', 'features.edu_games', 'features.private_post', 'features.limit_attend_type', 'features.chatbot']}
]
# for student in students:
#     student_id = student['id']
#     full_name = student['full_name']
#     print(f"ID: {student_id}, Full Name: {full_name}")
df = pd.DataFrame(students)

# Access 'id' and 'full_name' columns
student_ids = df['id']
full_names = df['full_name']
students_text = ""
# Iterate over the dataframe rows
# for index, row in df.iterrows():
#     student_id = row['id']
#     full_name = row['full_name']
students_text = "\n".join([f"{i+1}. ID: {student['id']}, Full Name: {student['full_name']}" for i, student in enumerate(students)])
print(students_text)
    # print(f"ID: {student_id}, Full Name: {full_name}")