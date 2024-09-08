## Các bước để cào dữ liệu trên batdongsan.com với Python và bộ thư viện Selenium:
+ Bước 1: Cài đặt các thư viện cần thiết trong file requirements.txt với cú pháp: pip install -r requirements.txt

+ Bước 2: Chạy lần lượt các file python sau:
   - B1_Gets_Links: Với file này, lựa chọn tên quân bạn muốn cào dữ liệu để cào các đường dẫn trong quận đó. Có thể tinh chỉnh với biến num_page là số max trang muốn cào, num_tabs là số tab Chrome được phép mở cùng lúc.
    
   - B2_Data_Scraper: Với file này, mã sẽ cào dữ liệu để lấy thông tin của từng đường dẫn đã lấy được sau khi chạy B1_Get_Links.py. Có thể tinh chỉnh với biến num_tabs là số tab Chrome được phép mở cùng lúc.

   - B3_Cleaner_Data: Với file này, mã sẽ làm sạch dữ liệu được lấy từ thư mục Raw_Data để điền vào các chỗ bị thiếu, thay đổi loại biến, thống nhất chuyển sang tiếng anh.

## Thư mục này chứa các code đã sử dụng để thu thập dữ liệu từ trang web batdongsan.com.vn
`Lưu ý:` 
+ Thư mục code đã được tách riêng ra sau khi cào dữ liệu, nếu muốn sử dụng code phải tạo các thư mục yêu cầu là:
   Raw_Data, Clean_Data và các thư mục con tỉnh thành bạn muốn cào. 

+ Code muốn sử dụng phải qua tinh chỉnh biến, giá trị đầu vào phù hợp.
   Thông tin chi tiết về code có ở link sau: https://github.com/QuangPVT/Scratch-Website-Data.git