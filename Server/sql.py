##### START DISHES #####
# %% ##### Cài đặt thư viện #####
import pandas as pd
import numpy as np
import os
import mysql.connector
from datetime import datetime, timedelta
from datetime import date, datetime, time
from collections import Counter


# Kết nối với cơ sở dữ liệu
host = "123.31.43.45"
database = "stg_ura_meta"
user = "stg_ura_meta"
password = "URA@Ur9UcwJ4fpkp7dD68hYfbcM74"

# Tạo đối tượng để kết nối với cơ sở dữ liệu
conn = mysql.connector.connect(
    host=host, database=database, user=user, password=password
)
# Tạo con trỏ để có thể thực hiện các phương thức truy vấn dữ liệu
cursor = conn.cursor()


# %%  Các function trong chương trình
# Đưa chuỗi thành câu theo quy tắc
def convert_to_sentence(text):
    words = text.split()
    sentence = " ".join(words)
    return sentence


# Lấy ra các món ăn theo mùa của table đã được pivot trước
def pivot_table(df, num_season):
    df_return = df[num_season]
    df_return = df_return.dropna()
    return df_return


# Lấy ra dataframe chứa danh sách món ăn và số lần xuất hiện của món ăn đó trong thực đơn.
def df_list_food_in_season(df_food):
    list_food = []
    for i in df_food:
        list_food_ = i.split(",")
        for j in list_food_:
            list_food.append(j.strip())
    element_counts = Counter(list_food)
    df_food = pd.DataFrame.from_dict(element_counts, orient="index", columns=["Count"])
    df_food = df_food.reset_index().rename(columns={"index": "name"})
    return df_food


# Thêm thông tin dinh dưỡng vào với từng món ăn và loại bỏ đi những món ăn không có trong danh sách món ăn tổng

def adding_nutrition(df_food, df_food_have_nutrition):
    
    df_food = pd.merge(df_food, df_food_have_nutrition, on='name', how='inner')
    return df_food


# Lấy mùa thực đơn của theo tháng
def get_season(num):
    season = int(num)
    if season >= 1 and season < 4:
        season = 1
    elif season >= 4 and season < 7:
        season = 2
    elif season >= 7 and season < 10:
        season = 3
    else:
        season = 4
    return season

# Tạo ra 1 dataframe với đầu vào là 1 bảng được pivot dữ liệu với mùa và list các thực đơn theo mùa
# Đầu ra của hàm này là 1 dataframe với các cột: tên các món ăn, số lần xuất hiện của các món ăn và thông tin dinh dưỡng liên quan
def get_dataframe_food(pivot_data_frame,df_dishes):
    # Tạo ra 3 dataframe trống để lưu dữ liệu
    data_frame_return = pd.DataFrame() # Dataframe return
    # Với thực đơn 100 ngày thì sẽ giao tối đa trong 2 mùa -> Tạo 2 dataframe ứng với mỗi mùa để thống kê
    df_season_1st = pd.DataFrame() 
    df_season_2nd = pd.DataFrame()
    try: # Với trường hợp thực đơn nằm trong 2 mùa 
        # Lấy danh sách các món ăn và số lần xuất hiện của các món ăn có trong thực đơn và chuyển về kiểu dữ liệu float64.
        df_season_1st = pivot_table(pivot_data_frame, pivot_data_frame.columns[0])
        df_season_1st = df_list_food_in_season(df_season_1st)
        df_season_2nd = pivot_table(pivot_data_frame, pivot_data_frame.columns[1])
        df_season_2nd = df_list_food_in_season(df_season_2nd)

        # Merge hai dataframe lại với nhau
        data_frame_return = pd.merge(
            df_season_1st, df_season_2nd, on="name", how="outer"
        )
        # Có những món ăn xuất hiện ở 1 mùa nhưng không xuất hiện ở mùa còn lại, 
        # Nên ta sẽ điền giá trị 0 vào đó
        data_frame_return = data_frame_return.fillna(0.0)
        # Có những món xuất hiện ở cả 2 mùa nên chúng ta sẽ lấy tổng của 2 món đó lại 
        data_frame_return["Count"] = (
            data_frame_return["Count_x"] + data_frame_return["Count_y"]
        )
        # Sau khi gộp lại ta bỏ đi số lần xuất hiện ở từng mùa tương ứng
        data_frame_return = data_frame_return.drop(["Count_x", "Count_y"], axis=1)

        
        #Đổi kiểu dữ liệu Count thành float ; thêm thông tin dinh dưỡng cho từng các món ăn và sắp xếp lại dataframe theo số lần xuât hiện và đánh lại index
        data_frame_return["Count"] = data_frame_return["Count"].astype("Float64")
        data_frame_return = adding_nutrition(data_frame_return, df_dishes)
        data_frame_return = data_frame_return.sort_values(by="Count", ascending=False)
        data_frame_return = data_frame_return.reset_index(drop=True)

    except:
        # Lấy danh sách các thực đơn có trong 1 mùa.
        data_frame_return = pivot_table(pivot_data_frame, pivot_data_frame.columns[0])
        # Lấy danh sách các món ăn và số lần xuất hiện của các món ăn có trong thực đơn và chuyển về kiểu dữ liệu float64.
        data_frame_return = df_list_food_in_season(data_frame_return)
        data_frame_return["Count"] = data_frame_return["Count"].astype("Float64")
        # Thêm thông tin dinh dưỡng cho từng các món ăn và sắp xếp lại dataframe theo số lần xuât hiện và đánh lại index
        data_frame_return = adding_nutrition(data_frame_return, df_dishes)
        data_frame_return = data_frame_return.sort_values(by="Count", ascending=False)
        data_frame_return = data_frame_return.reset_index(drop=True)

    return data_frame_return


# Đưa chuối về dữ liệu thời gian (datatime)
def convert_to_time (str_date):
  date_string = str_date
  # Convert string to datetime
  datetime_object = datetime.strptime(date_string, "%d/%m/%Y")
  return datetime_object

# Đưa chuối về dữ liệu thời gian (date)
def convert_to_date(date):
    # Convert datetime back to string in the desired format
    formatted_date = date.strftime("%d/%m/%Y")
    return formatted_date





# Loại bỏ đi những dấu ";" thành dấu ","
def make_sentence(df_his):
    # list_food_hist = food_hist.split(";")
    for i in df_his.index:
        df_his["buatrua"][i] = convert_to_sentence(df_his["buatrua"][i])
    df_his["buatrua"] = [word.replace("; ", ",") for word in df_his["buatrua"]]


# %% Dữ liệu đầu vào
def get_input():
    # print("Nhập ngày theo định dạng: YYYY-MM-DD")
    # date = input("--> 1. Nhập ngày dự đoán: ")
    # unit_id= input("--> 2. Chọn mã trường học: ")
    # group_id = input("--> 3. Chọn nhóm học sinh: ")
    # student_id = input("--> 4. Chọn học sinh: ")

    date = "2023-05-26"
    unit_id = "13047"
    group_id = "5"
    student_id = "26-05-2023"
    return date, unit_id, group_id, student_id


# %% dishes - Các món ăn trong cơ sở dữ liệu
def get_dishes():
    # Khởi tạo câu truy vấn với bảng món ăn bằng con trỏ (cursor)
    cursor.execute("SELECT * FROM dishes_analytics_copy1")

    # Lấy tất cả các hàng từ câu truy vấn
    rows = cursor.fetchall()

    # Lấy tất cả các cột/trường thuộc dữ liệu đã lấy từ câu truy vấn
    column_names = [column[0] for column in cursor.description]

    # Tạo dataframe df_sql_dishes từ "rows" và "column_names"
    df_sql_dishes = pd.DataFrame(rows, columns=column_names)

    # Tạo 1 dataframe "df_dishes" là bản sao của "df_sql_dishes"
    df_dishes = df_sql_dishes
    # print(df_dishes.tail(10))
    ## Xóa hàng cuối cùng trong dataframe, nếu dữ liệu có dấu hiêu dư thừa hoặc cần loại bỏ
    ## df_dishes = df_dishes.drop(df_dishes.index[-1])

    # Lấy ra những cột của dataframe
    cols_df_dishes = list(df_dishes.columns)

    # Loại bỏ đi những cột/trường không cần thiết khi làm việc với dataframe
    df_dishes = df_dishes.drop(
        columns=["id", "unit_id", "group_ids", "area_ids", "food_names"]
    )

    # Đưa các rows trong dataframe thành chữ in thường (lower)
    df_dishes["name"] = df_dishes["name"].str.lower()
    # Loại bỏ đi các khoảng trắng thauwf trong dataframe

    # Loại bỏ đi các hàng có chứa các kí tự "td1"; "td4"; "_"; "-"; "vt."; ".vt"; "+"; "mb."; "hn."; "("; ")"; ","; "."; ":";
    df_dishes["name"] = [word.replace("td1.", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("td4.", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("_", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("-", "") for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("–", "") for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("vt.", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace(".vt", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("+", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("mb.", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("hn.", " ", 1) for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace("(", " ") for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace(")", " ") for word in df_dishes["name"]]
    df_dishes["name"] = [word.replace(",", " ") for word in df_dishes["name"]]
    df_dishes["name"] = [" ".join(x.split()) for x in df_dishes["name"]]
    df_dishes = df_dishes[~(df_dishes["name"].str.contains("tham quan"))]
    df_dishes = df_dishes[~(df_dishes["name"].str.contains("buffe"))]
    df_dishes = df_dishes.drop_duplicates(subset="name")
    df_dishes = df_dishes.reset_index(drop=True)
    df_dishes["name"] = df_dishes["name"].apply(convert_to_sentence)
    clear = lambda: os.system("cls")
    clear()
    return df_dishes


# %% History - Lịch sử ăn uống của các em học sinh
def get_history(group_id, unit_id):
    # Câu truy vấn lấy ra lịch sử ăn uống theo "group_id" và "unit_id"
    query = "SELECT * FROM dishes_histories_copy1 where group_id = {0} and unit_id = {1}".format(
        group_id, unit_id
    )
    # Khởi tạo con trỏ (cursor) để truy vấn dữ liệu
    cursor.execute(query)

    # Lấy ra các hàng sau khi truy vấn dữ liệu
    rows = cursor.fetchall()

    # Lấy ra các cột/trường mà cursor lấy dữ liệu ra
    column_names = [column[0] for column in cursor.description]

    # Tạo ra dataframe "df_sql_history" từ các hàng và cột lấy từ rows và columns_names
    df_sql_histoy = pd.DataFrame(rows, columns=column_names)
    # Tạo "df_history"   là bản sao của "df_sql_histoy"
    df_history = df_sql_histoy
    df_history.isna().sum()
    cols_df_history = list(df_history.columns)
    # Bỏ đi các cột dữ liệu mà chúng ta không làm việc
    df_history = df_history.drop(
        columns=[
            "id",
            "name",
            "buasang",
            "buachieu",
            "buaphu",
            "school_point",
            "is_main",
            "created_at",
            "updated_at",
            "total_student",
            "total_money",
            "total_protein",
            "total_fat",
            "total_sugar",
            "total_calo",
            "food_names",
        ]
    )
    # Đưa các rows trong dataframe thành chữ in thường (lower)
    df_history["buatrua"] = df_history["buatrua"].str.lower()

    # Loại bỏ đi những khoảng trắng thừa ở đầu câu và cuối câu
    df_history["buatrua"] = [" ".join(x.split()) for x in df_history["buatrua"]]
    # df_history['buatrua'][1]

    # df_history['buatrua']

    list_hist = df_history["buatrua"][1]

    text = convert_to_sentence(list_hist)

    # print(text)
    df_history_test = df_history

    df_history_test = df_history_test[
        ~(df_history_test["buatrua"].str.contains("buffe"))
    ]
    df_history_test["buatrua"] = [
        word.replace(",", " ") for word in df_history_test["buatrua"]
    ]
    df_history_test = df_history_test[~(df_history_test["buatrua"].str.contains("hs"))]
    # print(df_history_test.tail(50))

    # # list_hist = df_history['buatrua'][1]
    make_sentence(df_history_test)
    # print(df_history_test['buatrua'].tail(50))
    df_history_test["buatrua"] = [
        " ".join(x.split()) for x in df_history_test["buatrua"]
    ]
    # # # print(sentence )
    # print(df_history_test.tail(50))

    # # df_history_test_2 = df_history

    df_history_test_2023 = df_history_test

    df_history_test_2023["date"] = ""

    for i in df_history_test_2023.index:
        time_obj = time(12, 0, 0)  # Example: 12:00:00
        df_history_test_2023["date"][i] = datetime.combine(
            df_history_test_2023["cdkp_date"][i], time_obj
        )
    # print(df_history_test_2023)
    clear = lambda: os.system("cls")
    clear()
    # return
    return df_history_test_2023


# %% Get suggestion

def get_suggestion(date_,unit_id,group_id, student_id_,df_history,df_dishes):

    df_history = get_history(group_id, unit_id)
    date = date_
    student_id = student_id_
    date_param = date.split("-")
    day = date_param[2]
    month = date_param[1]
    year = date_param[0]
    date_recomment = day + "/"+month+"/"+year
    date_recomment = convert_to_time(date_recomment)
    days_to_subtract = 7
    result_date = date_recomment - timedelta(days=days_to_subtract)

    # %% Lấy dữ liệu theo mùa mang ngày đang dự đoán
    df_100_in_season = df_history[
        df_history["season"].astype(int) == get_season(month)
    ]

    # Sắp xếp dataframe theo ngày gần nhất

    df_100_in_season = df_100_in_season.sort_values(by='date', ascending=False)

    # Lấy 100 bản ghi gần nhất để làm dữ liệu so sánh
    df_100_in_season = df_100_in_season.head(100)
    df_100_in_season = df_100_in_season.reset_index(drop = True)    
    
    # Tạo 1 dataframe với thông tin các món ăn trong 1 bữa theo 1 mùa
    pivot_df_100_food = df_100_in_season.pivot(
        index="cdkp_date", columns="season", values="buatrua"
    )
    pivot_df_100_food = pivot_df_100_food.sort_values(by="cdkp_date", ascending=False)
    
    # Tạo dataframe với thực đơn được thống kê với pivot 100 ngày bên trên
    df_100_after_counting = get_dataframe_food(pivot_df_100_food,df_dishes)
    # print(df_100_after_counting.head(50))


    # Lấy danh sách các ngày gần nhất
    df_40_at_least = df_history.sort_values(by="date", ascending=False)
    df_40_at_least = df_40_at_least.reset_index(drop=True)
    # print(df_40_at_least.head(50))

    # Lấy các ngày nhỏ hơn ngày dự đoán - 7
    df_7days_at_least_food_remove = df_40_at_least[
        df_40_at_least["date"] >= result_date
    ]
    # print(df_7days_at_least_food_remove.head(50))

    # Lấy 40 ngày gần nhất trong thực đơn
    df_40days_at_least = df_40_at_least.drop(index=df_7days_at_least_food_remove.index)
    df_40days_at_least = df_40days_at_least.reset_index(drop=True)
    df_40days_at_least = df_40days_at_least.head(40)
    # print(df_40days_at_least.head(50))

    # Tạo table được pivot theo mùa, vì 40 ngày gần nhất có thể giao giữa 2 mùa
    pivot_df_40days = df_40days_at_least.pivot(
        index="date", columns="season", values="buatrua"
    )
    # print(pivot_df_40days.head(40))


    
    # Tạo dataframe với list thực đơn được thống kê với pivot 40 ngày bên trên
    df_40_after_counting = get_dataframe_food(pivot_df_40days,df_dishes)
    # print(df_40_after_counting)


    # Tạo table được pivot theo mùa, với 7 ngày gần nhát, để loại bỏ đi những món ăn không dự đoán, sau đó tạo dataframe với list thực đơn đó
    pivot_df_7days = df_7days_at_least_food_remove.pivot(
        index="date", columns="season", values="buatrua"
    )
    df_7days_remove_after_counting = get_dataframe_food(pivot_df_7days,df_dishes)
    # print(df_7days_remove_after_counting)

    # Tính toán để đưa ra gợi ý món ăn
    ## Với 100 ngày gần nhất trong 1 mùa
    df_100_2023 = df_100_after_counting.sort_values(by="Count", ascending=False)
    df_100_2023 = df_100_2023.reset_index(drop=True)
    df_100_2023["Count"] = df_100_2023["Count"].astype(float)
    # print(df_100_2023.head(100))


    ## Với 40 ngày gần nhất
    df_40_2023_sorted = df_40_after_counting.sort_values(by="Count", ascending=False)
    df_40_2023_sorted = df_40_after_counting.reset_index(drop=True)
    # print(df_40_2023_sorted.head(40))

    # Merge 100 ngày với 40 ngày, với how="outer"

    merged_df = df_100_2023.merge(df_40_2023_sorted, on="name", how="outer")
    # merged_df
    merged_df["Count_x"].fillna(0, inplace=True)
    merged_df["Count_y"].fillna(0, inplace=True)
    # print(merged_df.head(40))
    

    # Điền thông tin các món ăn có ở dataframe 100 mà không có ở dataframe 40 và ngược lại 
    # # # ### Fill value from 40days to 100days

    merged_df_2 = merged_df

    # Những món chưa có trong X (100) sẽ lấy dữ liệu dinh dưỡng từ bên Y(40)
    merged_df_2["category_ids_x"] = merged_df_2["category_ids_y"].fillna(
        merged_df_2["category_ids_x"]
    )
    merged_df_2["protein_x"] = merged_df_2["protein_y"].fillna(merged_df_2["protein_x"])
    merged_df_2["fat_x"] = merged_df_2["fat_y"].fillna(merged_df_2["fat_x"])
    merged_df_2["sugar_x"] = merged_df_2["sugar_y"].fillna(merged_df_2["sugar_x"])
    merged_df_2["calo_x"] = merged_df_2["calo_y"].fillna(merged_df_2["calo_x"])
    # print(merged_df_2.head(40))

    # # # ### Fill value from 100days to 40days

    # # Những món chưa có trong Y(40) sẽ lấy dữ liệu dinh dưỡng từ bên X(100)
    merged_df_2["category_ids_y"] = merged_df_2["category_ids_x"].fillna(
        merged_df_2["category_ids_y"]
    )
    merged_df_2["protein_y"] = merged_df_2["protein_x"].fillna(merged_df_2["protein_y"])
    merged_df_2["fat_y"] = merged_df_2["fat_x"].fillna(merged_df_2["fat_y"])
    merged_df_2["sugar_y"] = merged_df_2["sugar_x"].fillna(merged_df_2["sugar_y"])
    merged_df_2["calo_y"] = merged_df_2["calo_x"].fillna(merged_df_2["calo_y"])
    # print(merged_df_2.tail(40))


    ###### Get the Inverse of the Count from x and y, to see the frequency of food in history.
    ## Lấy nghịch đảo của số lần xuât hiện của các món ăn trong vòng 40 và 100 ngày.

    merged_df_2["Count_y"] = 1 / merged_df_2["Count_y"]
    merged_df_2["Count_x"] = 1 / merged_df_2["Count_x"]
    # print(merged_df_2.tail(40))


    # Đây là những món KHÔNG có trong 100 ngày của mùa dự đoán, nó lại xuất hiện trong 40 ngày gần nhất. Tức các món này sẽ là các món giao mùa với mùa hiện tại -> Ta cần BỎ những món ăn này.

    merged_df_isnt_100days = merged_df_2
    merged_df_2_test = merged_df_2
    # Vì những món chưa xuất hiện nên khi ta lấy nghịch đảo (Inverse) thì 1/0 sẽ là inf(infinity) - vô cùng. Ta sẽ dùng mask (chỉ một giá trị boolean để compare và so sánh với các giá trị khác)
    inf_mask_merged_df_isnt_100days = np.isinf(merged_df_isnt_100days["Count_x"])
    # Sau khi lọc qua mask ta sẽ lấy được những món ăn không xuất hiện trong 100 ngày.
    merged_df_isnt_100days = merged_df_isnt_100days[inf_mask_merged_df_isnt_100days]
    # print(merged_df_isnt_100days)


    # Đây là những món KHÔNG có trong 40 ngày gần nhất, nhưng lại có trong 100 ngày của mùa đang dự đoán. Tức là các món trong 100 ngày gần nhất chưa xuất hiện hết -> Ta cần GIỮ lại các món ăn này.
    merged_df_isnt_40days = merged_df_2
    inf_mask_merged_df_isnt_40days = np.isinf(merged_df_isnt_40days["Count_y"])
    merged_df_isnt_40days = merged_df_isnt_40days[inf_mask_merged_df_isnt_40days]
    # print(merged_df_isnt_40days)


    # Danh sách các món ăn trong 7 ngày gần nhất cần loại. 
    list_food_remove = df_7days_remove_after_counting["name"]
    # print(list_food_remove)



    # Danh sách các món ăn sau khi loại các món ăn không có trong 100 ngày và 40 ngày. 
    merged_df_2_test = merged_df_2
    merged_df_2_test = merged_df_2_test[~inf_mask_merged_df_isnt_40days]
    merged_df_2_test = merged_df_2_test[~inf_mask_merged_df_isnt_100days]
    merged_df_2_test = merged_df_2_test.reset_index(drop=True)
    merged_df_2_test["weight"] = (
        merged_df_2_test["Count_y"] - merged_df_2_test["Count_x"]
    )
    # print(merged_df_2_test.head(50))

    merged_df_2_test = merged_df_2_test.sort_values(
        by=["category_ids_x", "Count_x"], ascending=False
    )
    merged_df_2_test = merged_df_2_test.reset_index(drop=True)
    # print(merged_df_2_test.head(50))
    

    # Danh sách các món ăn sau sau khi thêm các món không có trong 40 ngày. 
    selected_rows = pd.concat([merged_df_2_test,merged_df_isnt_40days], ignore_index=True)
    selected_rows = selected_rows.sort_values(by=['category_ids_x','weight'],ascending=False)
    selected_rows['weight'].fillna(1.0,inplace= True)
    selected_rows = selected_rows.reset_index(drop = True)
    # print(selected_rows.head(50))

    # Loại bỏ những món nằm trong 7 ngày gần nhất

    merged_df_2_test_check = selected_rows
    # print(merged_df_2_test_check.head(50))
    # print(list_food_remove)
    list_checked = []
    for i in selected_rows.index:
        if any(selected_rows["name"][i] == item for item in list_food_remove):
            if (
                int(selected_rows["category_ids_x"][i]) == 3
                or int(selected_rows["category_ids_x"][i]) == 2
                
            ):
                list_checked.append(i)
    # print(list_food_remove)
    # print(list_checked)
    # print(len(list_checked))


    merged_df_2_test_check = merged_df_2_test_check.drop(list_checked)
    merged_df_2_test_check = merged_df_2_test_check.reset_index(drop=True)
    # print(merged_df_2_test_check.head(50))

    # Modify lại các trường thông tin để hiện thị các thông tin cần thiết
    new_columns = {
        "category_ids_x": "category",
        "protein_x": "protein",
        "fat_x": "fat",
        "sugar_x": "sugar",
        "calo_x": "calo",
        "Count_x": "count_100",
        "Count_y": "count_40",
    }
    merged_df_2_show = merged_df_2_test_check[
        [
            "name",
            "Count_x",
            "Count_y",
            "category_ids_x",
            "protein_x",
            "fat_x",
            "sugar_x",
            "calo_x",
            "weight",
        ]
    ]
    merged_df_2_show = merged_df_2_show.rename(columns=new_columns)
    
    # print(merged_df_2_show.head(50))


    # merged_df_2_test_calo = (
    #     merged_df_2_show.sort_values(["category", "weight"], ascending=[True, False])
    #     .groupby("category")
    #     .head(2)
    # )
    # merged_df_2_test_calo = (
    #     merged_df_2_show.sort_values(["category", "weight"], ascending=[True, False])
    #     .groupby("category")
        
    # )
    # clear = lambda: os.system("cls")
    # clear()

    merged_df_2_test_calo = merged_df_2_show.reset_index(drop=True)
    merged_df_2_test_calo['category'] = merged_df_2_test_calo['category'].astype(int)
    merged_df_2_test_calo['fat'] = merged_df_2_test_calo['fat'].astype("Float64")
    merged_df_2_test_calo['sugar'] = merged_df_2_test_calo['sugar'].astype("Float64")
    merged_df_2_test_calo['calo'] = merged_df_2_test_calo['calo'].astype("Float64")
    merged_df_2_test_calo['protein'] = merged_df_2_test_calo['protein'].astype("Float64")
    merged_df_2_test_calo['count_100'] = merged_df_2_test_calo['count_100'].astype("Float64")
    merged_df_2_test_calo['count_40'] = merged_df_2_test_calo['count_40'].astype("Float64")
    # print(merged_df_2_test_calo)
    merged_df_2_test_calo_auto = merged_df_2_show.sort_values(['category', 'weight'], ascending=[True, False]).groupby('category').head(2).reset_index(drop=True)
    # merged_df_2_test_calo_auto = merged_df_2_test_calo.reset_index(drop=True)
    
    return merged_df_2_test_calo, merged_df_2_test_calo_auto


# %% Calculating Calories
def calculating_calories(data,calo_range):
    calos = calo_range.split("-")
    calo_min = int(calos[0])
    calo_max = int(calos[1])
    break_point = 0
    result = data
    while(break_point==0):
            # Lọc và lấy mẫu từng nhóm
            group_1 = data[data['category'] == 1].sample(n=1)
            group_2 = data[data['category'] == 2].sample(n=1)
            group_3 = data[data['category'] == 3].sample(n=2)

            # group_1 = data[data['category'] == 1].nlargest(1, 'weight')
            # group_2 = data[data['category'] == 2].nlargest(1, 'weight')
            # group_3 = data[data['category'] == 3].nlargest(2, 'weight')
            # Ghép các mẫu lại thành DataFrame kết quả
            result = pd.concat([group_1, group_2, group_3])

            # Kiểm tra tổng của 4 hàng
            total = result['calo'].sum()
            break_point = 0
            if calo_min < total < calo_max:
                break_point = 1
    result = result.reset_index(drop=True)
    return result, total

# %% Run Program
# date, unit_id, group_id, student_id = get_input()
# df_dishes = get_dishes()
# df_history = get_history(group_id, unit_id)
# give_suggestion = get_suggestion(date, unit_id, group_id, student_id,df_history,df_dishes)


# %% Call API
def api_get_suggestion(date, unit_id, group_id, student_id, calo_range):
    # date, unit_id, group_id, student_id = get_input()
    df_dishes = get_dishes()
    df_history = get_history(group_id, unit_id)
    give_suggestion, auto_give_suggestion  = get_suggestion(date, unit_id, group_id, student_id,df_history,df_dishes)
    cal_calories_results, total_calo = calculating_calories(give_suggestion,calo_range)
    return cal_calories_results 
# recommend,auto_recomned,total_calo = api_get_suggestion()

# print(recommend)


