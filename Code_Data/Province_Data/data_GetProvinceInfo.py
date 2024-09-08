from bs4 import BeautifulSoup
from unidecode import unidecode
import pandas as pd
import csv
import os

html_string_HCM = '''
<ul class="re__listing-search-select-list"><li class="re__option js__option re__checked" value="72"><span>Bình Chánh</span></li><li class="re__option js__option" value="65"><span>Bình Tân</span></li><li class="re__option js__option" value="66"><span>Bình Thạnh</span></li><li class="re__option js__option" value="73"><span>Cần Giờ</span></li><li class="re__option js__option" value="74"><span>Củ Chi</span></li><li class="re__option js__option" value="67"><span>Gò Vấp</span></li><li class="re__option js__option" value="75"><span>Hóc Môn</span></li><li class="re__option js__option" value="76"><span>Nhà Bè</span></li><li class="re__option js__option" value="68"><span>Phú Nhuận</span></li><li class="re__option js__option" value="53"><span>Quận 1</span></li><li class="re__option js__option" value="62"><span>Quận 10</span></li><li class="re__option js__option" value="63"><span>Quận 11</span></li><li class="re__option js__option" value="64"><span>Quận 12</span></li><li class="re__option js__option" value="54"><span>Quận 2</span></li><li class="re__option js__option" value="55"><span>Quận 3</span></li><li class="re__option js__option" value="56"><span>Quận 4</span></li><li class="re__option js__option" value="57"><span>Quận 5</span></li><li class="re__option js__option" value="58"><span>Quận 6</span></li><li class="re__option js__option" value="59"><span>Quận 7</span></li><li class="re__option js__option" value="60"><span>Quận 8</span></li><li class="re__option js__option" value="61"><span>Quận 9</span></li><li class="re__option js__option" value="69"><span>Tân Bình</span></li><li class="re__option js__option" value="70"><span>Tân Phú</span></li><li class="re__option js__option" value="71"><span>Thủ Đức</span></li></ul>
'''

html_string_HN = '''
<ul class="re__listing-search-select-list"><li class="re__option js__option re__checked" value="2"><span>Ba Đình</span></li><li class="re__option js__option" value="18"><span>Ba Vì</span></li><li class="re__option js__option" value="718"><span>Bắc Từ Liêm</span></li><li class="re__option js__option" value="7"><span>Cầu Giấy</span></li><li class="re__option js__option" value="24"><span>Chương Mỹ</span></li><li class="re__option js__option" value="20"><span>Đan Phượng</span></li><li class="re__option js__option" value="10"><span>Đông Anh</span></li><li class="re__option js__option" value="3"><span>Đống Đa</span></li><li class="re__option js__option" value="11"><span>Gia Lâm</span></li><li class="re__option js__option" value="15"><span>Hà Đông</span></li><li class="re__option js__option" value="4"><span>Hai Bà Trưng</span></li><li class="re__option js__option" value="21"><span>Hoài Đức</span></li><li class="re__option js__option" value="1"><span>Hoàn Kiếm</span></li><li class="re__option js__option" value="8"><span>Hoàng Mai</span></li><li class="re__option js__option" value="9"><span>Long Biên</span></li><li class="re__option js__option" value="17"><span>Mê Linh</span></li><li class="re__option js__option" value="29"><span>Mỹ Đức</span></li><li class="re__option js__option" value="14"><span>Nam Từ Liêm</span></li><li class="re__option js__option" value="27"><span>Phú Xuyên</span></li><li class="re__option js__option" value="19"><span>Phúc Thọ</span></li><li class="re__option js__option" value="22"><span>Quốc Oai</span></li><li class="re__option js__option" value="12"><span>Sóc Sơn</span></li><li class="re__option js__option" value="16"><span>Sơn Tây</span></li><li class="re__option js__option" value="6"><span>Tây Hồ</span></li><li class="re__option js__option" value="23"><span>Thạch Thất</span></li><li class="re__option js__option" value="25"><span>Thanh Oai</span></li><li class="re__option js__option" value="13"><span>Thanh Trì</span></li><li class="re__option js__option" value="5"><span>Thanh Xuân</span></li><li class="re__option js__option" value="26"><span>Thường Tín</span></li><li class="re__option js__option" value="28"><span>Ứng Hòa</span></li></ul>
'''

data ={
    'html_string': [html_string_HCM, html_string_HN],
    'provinceId': ['SG', 'HN'],
    'provinceName': ['HoChiMinh', 'HaNoi']
}

df_info = pd.DataFrame(data)

for index, col in df_info.iterrows():
    html_string = col['html_string']
    provinceId = col['provinceId']
    provinceName = col['provinceName']

    soup = BeautifulSoup(html_string, 'html.parser')

    # Tìm tất cả các thẻ <li> trong đoạn mã
    list_items = soup.find_all('li', class_='re__option')

    # Khởi tạo danh sách để lưu trữ các cặp tên quận/huyện và mã value tương ứng
    wardName = []
    wardId = []

    # Duyệt qua từng thẻ <li> và lấy thông tin tên quận/huyện và mã value
    for li in list_items:
        name = li.span.text.lower().replace(' ', '-')  # Lấy tên quận/huyện, chuyển về dạng viết thường và thay khoảng trắng bằng dấu '-'
        name = unidecode(name)  # Chuyển đổi sang viết thường không dấu bằng unidecode
        wardName.append(name)
        wardId.append(li['value'])  # Lưu mã value của quận/huyện

    # Lấy đường dẫn thư mục hiện tại chứa mã nguồn
    current_directory = os.path.dirname(os.path.abspath(__file__ if '__file__' in locals() else sys.argv[0]))

    # Đường dẫn đến thư mục chứa file CSV
    csv_directory = os.path.join(current_directory, 'Province_Data')
    
    # Kiểm tra xem thư mục có tồn tại không, nếu không thì tạo mới
    if not os.path.exists(csv_directory):
        os.makedirs(csv_directory)
    
    # Đường dẫn đến file CSV
    csv_file_path = os.path.join(csv_directory, provinceName + '_ward_data.csv')

    # Ghi dữ liệu vào file CSV
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        # Tạo writer object
        writer = csv.writer(file)
        
        # Viết header
        writer.writerow(['provinceId', 'provinceName', 'wardName', 'wardId'])
        
        # Viết dữ liệu
        for name, _id in zip(wardName, wardId):
            writer.writerow([provinceId, provinceName, name, _id])

    print("Dữ liệu " + provinceName + " đã được lưu vào file CSV.")