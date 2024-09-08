import json
import pandas as pd
import os
from unidecode import unidecode

district_name = ['HaNoi_T5', 'HCM_T5']

type_name = ['dat-dat-nen']
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

for dis_name in district_name:
    for typ_name in type_name:
        rel_path = "Raw_Data/" + dis_name + "/" + typ_name + "/data-raw-all.csv"
        folder_path = os.path.join(script_dir, rel_path)

        df = pd.read_csv(folder_path)

        # Loại bỏ các cột dữ liệu null
        if typ_name != 'dat-dat-nen':
            df = df.dropna()
        else:
            df = df.drop(['bedroom', 'toilet'], axis='columns')
            df = df.dropna()

        df.info(verbose=True)

        # Hàm kiểm tra chuỗi có chứa 2 dấu chấm, 2 dấu phẩy hoặc cả chấm lẫn phẩy
        def has_multiple_delimiters(area):
            if pd.notna(area):
                # Kiểm tra điều kiện: chứa ít nhất 2 dấu chấm hoặc 2 dấu phẩy hoặc cả chấm lẫn phẩy
                if area.count('.') >= 2 or area.count(',') >= 2 or ('.' in area and ',' in area):
                    return True
            return False

        # Áp dụng hàm kiểm tra cho cột 'area'
        df['invalid_area'] = df['area'].apply(has_multiple_delimiters)
        # Loại bỏ các dòng có giá trị 'True' trong cột 'invalid_area'
        df = df[~df['invalid_area']].drop(columns=['invalid_area'])

        # Hàm loại bỏ đơn vị 'm²' và chuyển đổi thành số thực
        def extract_float_number(area):
            if pd.notna(area):
                return float(area.split(' ')[0].replace(',', '.'))
            else:
                return None

        # Áp dụng hàm cho cột 'area'
        df['area'] = df['area'].apply(extract_float_number)
        df['pricePerM2'] = df['pricePerM2'].apply(extract_float_number)

        # Hàm chuyển đổi giá trị sang đơn vị triệu VNĐ
        def convert_to_million_vnd(price, area):
            if '/' in price:
                return None  # Trường hợp giá được chia cho diện tích, sẽ xử lý sau
            elif 'tỷ' in price:
                price_number = float(price.replace(' tỷ', '').replace(',', '.'))
                return price_number * 1000
            elif 'triệu' in price:
                price_number = float(price.replace(' triệu', '').replace(',', '.'))
                return price_number
            else:
                return None

        # Áp dụng hàm cho cột 'price'
        df['price'] = df.apply(lambda row: convert_to_million_vnd(row['price'], row['area']), axis=1)

        df.info(verbose=True)

        if dis_name == 'HCM_T5':
            districts_df = pd.read_csv(os.path.join(script_dir, "Province_Data/HoChiMinh_ward_data.csv"))
            # Thực hiện phép nối (merge) để thêm cột 'districtName' vào DataFrame gốc
            df = pd.merge(df, districts_df[['districtId', 'districtName']], on='districtId', how='left')
        else:
            districts_df = pd.read_csv(os.path.join(script_dir, "Province_Data/HaNoi_ward_data.csv"))
            # Thực hiện phép nối (merge) để thêm cột 'districtName' vào DataFrame gốc
            df = pd.merge(df, districts_df[['districtId', 'districtName']], on='districtId', how='left')

        df.to_csv(script_dir + '/Clean_Data/' + dis_name + '/' + typ_name + '_' + dis_name + '_all.csv', encoding='utf-8', index=False)