import os
import re
import json
import time
import pandas as pd
import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from queue import Queue
from datetime import date
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from bs4 import BeautifulSoup

# Lấy đường dẫn của thư mục hiện tại
current_directory = os.path.dirname(os.path.abspath(__file__ if '__file__' in locals() else sys.argv[0]))
# Xác định đường dẫn đến thư mục Province_Data
province_data_directory = os.path.join(current_directory, 'Province_Data')
# Kiểm tra nếu thư mục 'data' không tồn tại thì tạo nó
if not os.path.exists(province_data_directory):
    os.makedirs(province_data_directory)
# Tạo đường dẫn đầy đủ đến thư mục 'Raw_Data'
data_directory = os.path.join(current_directory, 'Raw_Data')
# Kiểm tra nếu thư mục 'data' không tồn tại thì tạo nó
if not os.path.exists(data_directory):
    os.makedirs(data_directory)

# Khởi tạo DataFrame df_full_data
column_names = ['productId', 'url', 'date', 'price', 'area', 'pricePerM2', 'type', 'bedroom', 'toilet', 'provinceId', 'districtId', 'wardId']
df_full_data = pd.DataFrame(columns=column_names)

###Khai báo biến###
url = "https://batdongsan.com.vn/ban-"
# all_home_type = ['nha-rieng-', 'can-ho-chung-cu-', 'dat-dat-nen-']
# all_provinceName = ['HoChiMinh', 'HaNoi']
all_home_type = ['dat-dat-nen-']
all_provinceName = ['HoChiMinh']
page_queue = Queue()
thread_lock = threading.Lock()

###Khai báo hàm###
# Hàm để cào dữ liệu từ một trang
def scrape_page(url):
    chrome_options = Options()
    chrome_options.add_argument("--disable-infobars")  # Tắt thanh thông tin Chrome
    chrome_options.add_argument("--disable-extensions")  # Tắt các tiện ích mở rộng
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    chrome_options.add_argument("--disable-popup-blocking")  # Disable popup blocking
    chrome_options.add_argument("--disable-sync")  # Disable syncing with Google account
    driver = webdriver.Chrome(options=chrome_options)
    width = 100
    height = 50
    driver.set_window_size(width, height)
    driver.get(url)
    driver.minimize_window()
    time.sleep(4)
    html_string = driver.page_source
    soup = BeautifulSoup(html_string, 'html.parser')
    driver.close()
    driver.quit()
    print("Đang cào: " + url)
    with thread_lock:
        # Bắt đầu cào dữ liệu mong muốn
        script_tags = soup.find_all('script', type='text/javascript')
        json_data = None

        for script_tag in script_tags:
            script_content = script_tag.string
            if script_content:
                if 'window.pageTrackingData' in script_content:
                    # Loại bỏ các ký tự không mong muốn để lấy chuỗi JSON
                    json_string = script_content.split("JSON.parse('", 1)[1].rsplit("')", 1)[0]

                    # Phân tích chuỗi JSON thành một đối tượng Python
                    json_data = json.loads(json_string)

        if json_data is None:
            return

        # Chuyển đổi dữ liệu thành DataFrame
        df_1 = pd.DataFrame(json_data['products'])


        # Loại bỏ các cột không mong muốn từ DataFrame
        columns_to_drop = ['intent', 'projectId', 'pageType', 'vipType', 'verified', 'expired', 'cateId', 'streetId', 'pageId', 'createByUser', 'productType']
        df_1 = df_1.drop(columns=columns_to_drop)

        # Tạo danh sách chứa dữ liệu từng biến
        full_urls = []
        prices = []
        areas = []
        price_per_m2s = []
        bedrooms = []
        toilets = []

        # Cắt bớt dữ liệu không cần thiết
        target_div = soup.find('div', class_='re__srp-list js__srp-list')
        # Tạo danh sách các thẻ HTML chứa thông tin bất động sản
        property_tags = target_div.find_all('div', 're__card-full')
        # Bắt đầu lấy dữ liệu

        # Duyệt qua từng thẻ để lấy dữ liệu
        for property_tag in property_tags:
            # Lấy đường dẫn
            a_tag = property_tag.find('a')
            href = a_tag['href']
            if href:
                full_urls.append(url + href)
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

        # Tạo DataFrame từ các danh sách dữ liệu
        df_2 = pd.DataFrame({
            'url': full_urls,
            'price': prices,
            'area': areas,
            'pricePerM2': price_per_m2s,
            'type': 'dat-dat-nen',
            'bedroom': bedrooms,
            'toilet': toilets,
            'date': date.today()
        })

        # Phép toán merge giữa df_1 và df_2 dựa trên index
        df = df_1.merge(df_2, left_index=True, right_index=True)

        # Tên các cột ban đầu
        columns_reindex = ['productId', 'url', 'date', 'price', 'area', 'pricePerM2', 'type', 'bedroom', 'toilet', 'cityCode', 'districtId', 'wardId']

        # Sắp xếp lại các cột trong DataFrame
        df = df.reindex(columns=columns_reindex)
        df = df.rename(columns = {'cityCode':'provinceId'})
        global df_full_data
        df_full_data = pd.concat([df_full_data, df], ignore_index=True)
        

def worker():
    while True:
        url = page_queue.get()
        if url is None:
            page_queue.task_done()
            break
        scrape_page(url)
        page_queue.task_done()

def start_scraper(main_url, wardName, max_page):
    # Số lượng trang muốn cào
    num_page = 50

    if (max_page < num_page):
        num_page = max_page

    # Số lượng mở tab selenium tối đa khi cào
    num_tabs = 8
    # Tạo danh sách các URL của các trang cần cào dữ liệu
    page_urls = [main_url + '/p' + str(i) for i in range(1, num_page + 1)]
    # Đưa các URL vào hàng đợi
    for url in page_urls:
        page_queue.put(url)

    # Tạo danh sách các thread để cào dữ liệu
    threads = []

    for _ in range(num_tabs):
        thread = threading.Thread(target=worker)
        threads.append(thread)

    # Khởi động các thread và chờ chúng hoàn thành
    for thread in threads:
        thread.start()

    # Chờ cho tất cả các URL được xử lý
    page_queue.join()

    # Tắt các thread khi hoàn thành
    for _ in range(num_tabs):
        page_queue.put(None)
    for thread in threads:
        thread.join()

    # Tên file txt
    file_name = 'data-raw-'+ wardName + '.csv'
    # Đường dẫn đầy đủ đến file csv
    file_path = os.path.join(data_directory, file_name)
    print("Khu vực " + wardName + " hiện có tổng số bất động sản đang bán là:", len(df_full_data))
    df_full_data.to_csv(file_path, index=False)
    print('----Done----')

# Hàm main
print("----Bắt đầu cào dữ liệu----")
for home_type in all_home_type:
    for provinceName in all_provinceName:

        # Đường dẫn tới file CSV dựa trên biến provinceName
        csv_file_path = os.path.join(province_data_directory, f'{provinceName}_ward_data.csv')

        # Đọc file CSV vào DataFrame
        df_ward_info = pd.read_csv(csv_file_path)

        for index, col in df_ward_info.iterrows():
            wardName = col['wardName']

            main_url = url + home_type + wardName
            data_directory = os.path.join(current_directory, 'Raw_Data')
            csv_all_done = [f for f in os.listdir(data_directory) if f.endswith('.csv')]
            check_done = False
            for csv_file in csv_all_done:
                if wardName in csv_file:
                    check_done = True
            if (check_done):
                print('Đã có dữ liệu ' + wardName + '!')
                continue
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
            
            time.sleep(4)
            html_string = driver.page_source
            soup = BeautifulSoup(html_string, 'html.parser')
            driver.close()
            driver.quit()

            max_page = None
            pagination_numbers = soup.find_all('a', class_='re__pagination-number')
            if len(pagination_numbers) == 0:
                max_page = 1
            else:
                
                for number_tag in pagination_numbers:
                    max_page = int(number_tag.get_text(strip=True))
            
            product_numbers = soup.find('span', id='count-number')
            if product_numbers.text == '0':
                print('Không có dữ liệu ' + wardName + ' trên website!')
                continue
                
            print("Khu vực " + wardName + " có tổng số " + str(max_page) + " trang")
            print("----Bắt đầu cào dữ liệu khu vực " + wardName + "----")
            start_scraper(main_url, wardName, max_page)


            