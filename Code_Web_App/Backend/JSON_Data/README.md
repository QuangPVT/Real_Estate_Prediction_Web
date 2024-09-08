## Giới thiệu về thư mục dữ liệu JSON_Data

Đây là thư mục chứa dữ liệu JSON phục vụ cho máy chủ Python Backend sử dụng để truy vấn query các thông tin liên quan đến mô hình học máy mà người dùng yêu cầu sử dụng.

## Các Cột Dữ Liệu Và Ý Nghĩa Trong File JSON

1. `model` (string): Tên model được đặt theo tên của tỉnh thành (VD: HCM_T5 hoặc HaNoi_T5)
2.  `type` (string): Loại bất động sản muốn dự đoán giá cả
3. `data_columns` (object): Mảng danh sách các chuỗi dùng để nêu tên cột của input đầu vào model học máy
4. `district_columns` (object): Mảng danh sách các chuỗi là tên quận huyện mà model hỗ trợ (Nếu input đầu vào không có trong danh sách, mặc định model dự đoán giá dựa trên toàn bộ dữ liệu không được chia nhóm theo quận huyện)
5. `model_accuracy` (float): Giá trị R² của model, 1 trong thông số đánh giá độ chính xác của model học máy dự đoán