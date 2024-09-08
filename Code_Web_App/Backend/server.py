from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import tempfile
import json
import os
import time
import numpy as np
import pandas as pd

app = Flask(__name__)
CORS(app)

# Tải các file models và JSON data
models = {
    "HCM_Home": {
        "model": pickle.load(open("Models/HCM_T5_nha-rieng_T5_2024_ML.pickle", "rb")),
        "type": json.load(open("JSON_Data/HCM_T5_nha-rieng_T5_2024_JSON.json"))["type"],
        "data_columns": json.load(open("JSON_Data/HCM_T5_nha-rieng_T5_2024_JSON.json"))["data_columns"],
        "district_columns": json.load(open("JSON_Data/HCM_T5_nha-rieng_T5_2024_JSON.json"))["district_columns"]
    },
    "HCM_Land": {
         "model": pickle.load(open("Models/HCM_T5_dat-dat-nen_T5_2024_ML.pickle", "rb")),
        "type": json.load(open("JSON_Data/HCM_T5_dat-dat-nen_T5_2024_JSON.json"))["type"],
        "data_columns": json.load(open("JSON_Data/HCM_T5_dat-dat-nen_T5_2024_JSON.json"))["data_columns"],
        "district_columns": json.load(open("JSON_Data/HCM_T5_dat-dat-nen_T5_2024_JSON.json"))["district_columns"]
    },
    "HN_Home": {
        "model": pickle.load(open("Models/HaNoi_T5_nha-rieng_T5_2024_ML.pickle", "rb")),
        "type": json.load(open("JSON_Data/HaNoi_T5_nha-rieng_T5_2024_JSON.json"))["type"],
        "data_columns": json.load(open("JSON_Data/HaNoi_T5_nha-rieng_T5_2024_JSON.json"))["data_columns"],
        "district_columns": json.load(open("JSON_Data/HaNoi_T5_nha-rieng_T5_2024_JSON.json"))["district_columns"]
    },
    "HN_Land": {
        "model": pickle.load(open("Models/HaNoi_T5_dat-dat-nen_T5_2024_ML.pickle", "rb")),
        "type": json.load(open("JSON_Data/HaNoi_T5_dat-dat-nen_T5_2024_JSON.json"))["type"],
        "data_columns": json.load(open("JSON_Data/HaNoi_T5_dat-dat-nen_T5_2024_JSON.json"))["data_columns"],
        "district_columns": json.load(open("JSON_Data/HaNoi_T5_dat-dat-nen_T5_2024_JSON.json"))["district_columns"]
    },
}

# Hàm dự báo giá cả bất động sản với các tham số đầu vào
def get_estimated_price(model, data_columns, district_name, district_columns, area, floors=None, bedroom=None, toilet=None, facade=None, furniture=None, status_doc=None, market=None, hospital=None, model_type='nha-rieng'):
    if model_type == 'dat-dat-nen':
        # Với model đất đai, ta chỉ có 2 cột input là area và district_name
        x = np.zeros(len(data_columns) + len(district_columns))
        x[0] = area
        try:
            loc_index = district_columns.index(district_name.lower())
            x[len(data_columns) + loc_index] = 1
        except ValueError:
            print(f"District '{district_name}' not found in district columns. Defaulting district columns to 0.")
        # Generate column names
        all_columns = data_columns[:1] + district_columns
        
    else:
        # Với model nhà riêng sẽ có thêm các biến khác
        x = np.zeros(len(data_columns) + len(district_columns))
        x[0] = area
        x[1] = floors if floors is not None else 0
        x[2] = bedroom if bedroom is not None else 0
        x[3] = toilet if toilet is not None else 0
        x[4] = facade if facade is not None else 0
        x[5] = furniture if furniture is not None else 0
        x[6] = status_doc if status_doc is not None else 0
        x[7] = market if market is not None else 0
        x[8] = hospital if hospital is not None else 0
        try:
            loc_index = district_columns.index(district_name.lower())
            x[len(data_columns) + loc_index] = 1
        except ValueError:
            print(f"District '{district_name}' not found in district columns. Defaulting district columns to 0.")
        all_columns = data_columns[:9] + district_columns
    
    x_df = pd.DataFrame([x], columns=all_columns)
    predicted_price = round(model.predict(x_df)[0], 1)
    return predicted_price

# Hàm phân tích dữ liệu BeautifulSoup thành dataframe
def get_dataframe(soup):
    # Tạo danh sách chứa dữ liệu từng biến
    product_ids = []
    full_urls = []
    prices = []
    areas = []
    price_per_m2s = []
    bedrooms = []
    toilets = []
    location = []
    published = []
    image_url = []

    # Cắt bớt dữ liệu không cần thiết
    target_div = soup.find('div', class_='re__srp-list js__srp-list')
    # Tạo danh sách các thẻ HTML chứa thông tin bất động sản
    property_tags = target_div.find_all('div', 're__card-full')
    # Bắt đầu lấy dữ liệu

    if property_tags == None:
        return [None]
 
    # Duyệt qua từng thẻ để lấy dữ liệu
    for index, property_tag in enumerate(property_tags):
        if index >= 20:
            break

        product_id_tag = property_tag.find('a', class_='js__product-link-for-product-id')
        if "link-promotion-ads" in str(product_id_tag):
            continue
        product_ids.append(product_id_tag.get('data-product-id') if product_id_tag else "N/A")

        # Lấy đường dẫn
        a_tag = property_tag.find('a')
        href = a_tag['href']
        if href:
            full_urls.append(href)
        # Lấy giá
        price_span = property_tag.find('span', class_='re__card-config-price')
        prices.append(price_span.text.strip() if price_span else "N/A")
        # Lấy diện tích
        area_span = property_tag.find('span', class_='re__card-config-area')
        areas.append(area_span.text.strip() if area_span else "N/A")
        # Lấy giá/diện tích
        price_per_m2_span = property_tag.find('span', class_='re__card-config-price_per_m2')
        price_per_m2s.append(price_per_m2_span.text.strip() if price_per_m2_span else "N/A")
        # Lấy số phòng ngủ
        bedroom_span = property_tag.find('span', class_='re__card-config-bedroom')
        bedrooms.append(bedroom_span.text.strip().split()[0] if bedroom_span else "N/A")
        # Lấy số phòng vệ sinh
        toilet_span = property_tag.find('span', class_='re__card-config-toilet')
        toilets.append(toilet_span.text.strip().split()[0] if toilet_span else "N/A")

        location_elem = property_tag.find('div', class_='re__card-location')
        location.append(location_elem.text.strip() if location_elem else "N/A")
        
        published_at_elem = property_tag.find('span', class_='re__card-published-info-published-at')
        published.append(published_at_elem.get('aria-label') if published_at_elem else "N/A")

        image_url_elem = property_tag.find('div', class_='re__card-image')
        img_tag = image_url_elem.find('img')
        if img_tag != None:
            temp = img_tag.get('data-img')
            image_url.append(temp)

    # Tạo DataFrame từ các danh sách dữ liệu
    df = pd.DataFrame({
        'product_id': product_ids,
        'url': full_urls,
        'price': prices,
        'area': areas,
        'pricePerM2': price_per_m2s,
        'bedroom': bedrooms,
        'toilet': toilets,
        'location': location,
        'published': published,
        'image_url': image_url
    })

    return df

# Hàm driver selenium để lấy dữ liệu thời gian thực từ trang web bất động sản
def run_driver(real_estate_url):
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-notifications")
    options.add_argument('--headless')
    options.add_argument('--log-level=3')
    options.add_argument('--window-size=800,600')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')

    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win64",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
    )

    driver.minimize_window()
    try:
        driver.get(real_estate_url)
        time.sleep(3)
        html_string = driver.page_source
        soup = BeautifulSoup(html_string, 'html.parser')
        return get_dataframe(soup)
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"
    finally:
        driver.close()
        driver.quit()

# Hàm khai báo các urls dùng để lấy dữ liệu thời gian thực
def get_full_data_recommend(main_url, type_name, sort_value, bedroom, area):
    urls = []
    if type_name == "nha-rieng":
        urls = [
            f"{main_url}/{int(bedroom)}pn/p{i}?dtnn={int(area-10)}m2&dtln={int(area+10)}m2&sortValue={int(sort_value)}"
            for i in range(1, 6)
        ]
    else:
        urls = [
            f"{main_url}/p{i}?dtnn={int(area-10)}m2&dtln={int(area+10)}m2&sortValue={int(sort_value)}"
            for i in range(1, 6)
        ]
        
    with ThreadPoolExecutor(max_workers=5) as executor:
        dataframes = list(executor.map(run_driver, urls))

    # Lọc bỏ các dataframe có giá trị None và chỉ giữ lại các DataFrame hợp lệ
    valid_dataframes = [df for df in dataframes if isinstance(df, pd.DataFrame)]
    
    if valid_dataframes:
        full_df = pd.concat(valid_dataframes, ignore_index=True)
    else:
        full_df = pd.DataFrame()  # Trả về dataframe rỗng nếu không có dataframe nào hợp lệ
    
    return full_df

# Làm sạch dữ liệu thời gian thực để tiến hành lọc, sắp xếp
def cleaner_dataframe(df):
    def extract_float_number(area):
            if pd.notna(area):
                # Tách phần số và phần ký hiệu
                num_str = area.split(' ')[0]
                # Nếu chuỗi chứa cả dấu ',' và dấu '.'
                if ',' in num_str and '.' in num_str:
                    num_str = num_str.replace(',', '')  # Bỏ dấu ','
                else:
                    num_str = num_str.replace(',', '.')  # Đổi dấu ',' thành '.'
                return float(num_str)
            else:
                return None

    # Áp dụng hàm cho cột 'area' và 'product_id'
    df['area'] = df['area'].apply(extract_float_number)
    df['product_id'] = df['product_id'].apply(extract_float_number)
    # Hàm chuyển đổi giá trị sang đơn vị triệu VNĐ
    def convert_to_million_vnd(price, area):
        if pd.notna(price) and price != 'Thoả thuận':
            if '/' in price:
                return None  # Trường hợp giá được chia cho diện tích, sẽ xử lý sau
            elif 'tỷ' in price:
                price_number = float(price.replace(' tỷ', '').replace(',', '.'))
                return price_number * 1000
            elif 'triệu' in price:
                price_number = float(price.replace(' triệu', '').replace(',', '.'))
                return price_number if price_number >= 100 else None
            else:
                return None
        else:
            return None

    # Hàm xử lý trường hợp giá được chia cho diện tích
    def handle_price_per_area(price, area):
        if pd.notna(price) and '/' in price and pd.notna(area):
            try:
                price_per_area = float(price.split('/')[0].replace(',', '.')) / float(area.replace(' m²', ''))
                return price_per_area
            except ValueError:
                return None
        else:
            return None

    # Áp dụng hàm cho cột 'price'
    df['price'] = df.apply(lambda row: convert_to_million_vnd(row['price'], row['area']), axis=1)

    # Nếu có trường hợp giá được chia cho diện tích, ta sẽ xử lý
    df['price'] = df.apply(lambda row: handle_price_per_area(row['price'], row['area']) if pd.isna(row['price']) else row['price'], axis=1)

    return df

# Hàm tiến hành sắp xếp dữ liệu
def sort_dataframe_by_cleaned(df, sort_value):
    # Tạo bản sao của DataFrame gốc
    df_original = df.copy()

    # Làm sạch dữ liệu
    df_cleaned = cleaner_dataframe(df.copy())

    # Chuyển đổi cột 'published' sang kiểu datetime
    df_cleaned['published'] = pd.to_datetime(df_cleaned['published'], format='%d/%m/%Y')
    df_original['published'] = pd.to_datetime(df_original['published'], format='%d/%m/%Y')

    # Sắp xếp theo sort_value
    if sort_value == 1:  # Tin mới nhất
        df_cleaned = df_cleaned.sort_values(by='published', ascending=False)
    elif sort_value == 2:  # Giá thấp đến cao
        df_cleaned = df_cleaned.sort_values(by='price', ascending=True)
    elif sort_value == 3:  # Giá cao đến thấp
        df_cleaned = df_cleaned.sort_values(by='price', ascending=False)
    elif sort_value == 4:  # Diện tích bé đến lớn
        df_cleaned = df_cleaned.sort_values(by='area', ascending=True)
    elif sort_value == 5:  # Diện tích lớn đến bé
        df_cleaned = df_cleaned.sort_values(by='area', ascending=False)

    # Sắp xếp lại DataFrame gốc dựa trên thứ tự của bản sao đã làm sạch
    df_sorted = df.loc[df_cleaned.index]

    return df_sorted

# Hàm API predict_price
@app.route('/predict_price', methods=['POST'])
def predict_price():
    data = request.json
    model_name = data.get('model')
    type_name = data.get('type')
    area = data.get('area')
    floors = data.get('floors')
    bedroom = data.get('bedroom')
    toilet = data.get('toilet')
    facade = data.get('facade')
    furniture = data.get('furniture')
    status_doc = data.get('status_doc')
    market = data.get('market')
    hospital = data.get('hospital')
    district_name = data.get('district_name')
    
    # Check for negative values
    if any(x is not None and x < 0 for x in [area, floors, bedroom, toilet, facade]):
        return jsonify({'error': 'Input values for area, floors, bedroom, toilet, and facade must be non-negative.'}), 400

        # Check for small values
    if any(x is not None and x < 20 for x in [area]):
        return jsonify({'error': 'Input values for area must be up to 20 meter square.'}), 400

    if any(x is not None and x < 2 for x in [facade]):
        return jsonify({'error': 'Input values for facade must be up to 2 meter.'}), 400

    if model_name == 'HCM_T5':
        if type_name == 'nha-rieng':
            model_info = models['HCM_Home']
        else:
            model_info = models['HCM_Land']
    else:
        if type_name == 'nha-rieng':
            model_info = models['HN_Home']
        else:
            model_info = models['HN_Land']
    
    model = model_info["model"]
    data_columns = model_info["data_columns"]
    district_columns = model_info["district_columns"]

    try:
        if type_name == 'dat-dat-nen':
            price = get_estimated_price(model, data_columns, district_name, district_columns, area, model_type=type_name)
        else:
            price = get_estimated_price(model, data_columns, district_name, district_columns, area, floors, bedroom, toilet, facade, furniture, status_doc, market, hospital, model_type=type_name)
        return jsonify({'message': 'Success', 
            'price': price, 
            'model_name': model_name, 
            'type_name':type_name, 
            'area': area, 
            'floors': floors, 
            'bedroom': bedroom, 
            'toilet': toilet, 
            'facade': facade, 
            'furniture': furniture, 
            'status_doc': status_doc, 
            'market': market, 
            'hospital': hospital, 
            'district_name': district_name})

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Hàm API recommend_listings
@app.route('/recommend_listings', methods=['GET'])
def recommend_listings():
    district_name = request.args.get('district_name')
    type_name = request.args.get('type')
    area = float(request.args.get('area'))
    bedroom = int(request.args.get('bedroom', 1))  # Default to 1 if not provided
    toilet = int(request.args.get('toilet', 1))  # Default to 1 if not provided
    sort_value = int(request.args.get('sort_value')) 
    # sort_value = 1 => Tin mới nhất
    # sort_value = 2 => Giá thấp đến cao
    # sort_value = 3 => Giá cao đến thấp
    # sort_value = 4 => Diện tích bé đến lớn
    # sort_value = 5 => Diện tích lớn đến bé

    url = 'https://batdongsan.com.vn/ban-'

    main_url = url + type_name + '-' + district_name

    recommended_listings = get_full_data_recommend(main_url, type_name, sort_value, bedroom, area)


    # Update the url column
    recommended_listings['url'] = recommended_listings['url'].apply(lambda x: main_url + x)

    # Update null values in 'image_url' column
    recommended_listings['image_url'].fillna('https://staticfile.batdongsan.com.vn/images/logo/standard/red/logo.svg', inplace=True)

    recommended_listings = recommended_listings[recommended_listings['area'] != "N/A"]

    recommended_listings_sorted = sort_dataframe_by_cleaned(recommended_listings, sort_value)

    recommended_listings_sorted = recommended_listings_sorted.drop_duplicates(subset='product_id', keep='first')

    recommended_listings_sorted = recommended_listings_sorted.head(50)

    recommendations = recommended_listings_sorted.to_dict(orient='records')

    return jsonify({'recommendations': recommendations})

if __name__ == '__main__':
    app.run(debug=True)