## Giới thiệu tập dữ liệu sạch về nhà riêng (Home_Clean)
Tập dữ liệu sau chứa thông tin về các thông tin bất động sản loại nhà riêng trên trang Website batdongsan.com.vn mà nhóm đã thu thập được.
Dữ liệu  có tên bắt đầu bằng "nha-rieng" trong mỗi thư mục tỉnh thành.

## Các Cột Dữ Liệu Và Ý NGhĩa

1. `productId` (int): Mã định danh duy nhất cho danh sách bất động sản.
2. `area` (float): Diện tích của bất động sản tính bằng mét vuông.
3. `price` (float): Giá của bất động sản tính bằng triệu VND.
4. `floors` (int): Số tầng của bất động sản.
5. `bedroom` (int): Số phòng ngủ của bất động sản.
6. `toilet` (int): Số nhà vệ sinh của bất động sản.
7. `facade` (float): Chiều rộng mặt tiền của bất động sản. Trường này có thể để trống.
8. `furniture` (bool): Thông tin về tình trạng nội thất. Trường này có thể để trống.
9. `status_doc` (bool): Tình trạng tài liệu của bất động sản (1 là có sẵn, 0 là không có sẵn).
10. `ggmap_e` (float): Tọa độ kinh độ của bất động sản trên Google Maps.
11. `ggmap_n` (float): Tọa độ vĩ độ của bất động sản trên Google Maps.
12. `product_link` (string): Đường dẫn URL đến danh sách bất động sản trên trang web.
13. `district_id` (int): ID của quận/huyện nơi bất động sản tọa lạc.
14. `market` (bool): Gần chợ (1 là gần, 0 là không gần).
15. `hospital` (bool): Gần bệnh viện (1 là gần, 0 là không gần).
16. `elevator` (bool): Có thang máy (1 là có, 0 là không).

`LƯU Ý:` Dữ liệu đã được làm sạch sẵn sàng cho việc đưa vào xây dựng mô hình học máy.
=================================

## Giới thiệu tập dữ liệu sạch về đất đai (Land_Clean)
Dataset này chứa thông tin về các danh sách đất nền thu thập từ trang Website batdongsan.com.vn
Dữ liệu  có tên bắt đầu bằng "dat-dat-nen" trong mỗi thư mục tỉnh thành.

## Các Cột Dữ Liệu Và Ý NGhĩa

1. `productId` (int): Mã định danh duy nhất cho danh sách bất động sản.
2. `url` (string): Đường dẫn URL đến danh sách bất động sản trên trang web.
3. `date` (date): Ngày đăng tải danh sách bất động sản.
4. `price` (float): Giá của bất động sản, có thể bao gồm cả đơn vị tiền tệ.
5. `area` (float): Diện tích của bất động sản tính bằng mét vuông.
6. `pricePerM2` (float): Giá trên mỗi mét vuông của bất động sản.
7. `type` (string): Loại bất động sản (ví dụ: đất nền).
8. `bedroom` (int): Số phòng ngủ của bất động sản (đối với loại hình bất động sản có phòng ngủ).
9. `toilet` (int): Số nhà vệ sinh của bất động sản (đối với loại hình bất động sản có nhà vệ sinh).
10. `provinceId` (int): Mã định danh của tỉnh/thành phố nơi bất động sản tọa lạc.
11. `districtId` (int): Mã định danh của quận/huyện nơi bất động sản tọa lạc.
12. `wardId` (int): Mã định danh của phường/xã nơi bất động sản tọa lạc.

`LƯU Ý:` Dữ liệu đã được làm sạch sẵn sàng cho việc đưa vào xây dựng mô hình học máy.
