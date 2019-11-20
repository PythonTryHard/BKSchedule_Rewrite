# BKSchedule Rewrite - Viết bởi SV Bách Khoa cho SV Bách Khoa
Vì gần đây app `BKSchedule` sập, `BKSchedule Rewrite` ra đời. 

Phần mềm nguồn mở theo bản quyền GNU GPL v3.0

## Tính năng
* Thời gian tìm thời khoá biểu nhanh (~5 giây) nhờ bỏ qua các bước load hình ảnh, JS, vv.
* Giao diện tương tác dòng lệnh mặc dù xa lạ nhưng bớt gồ ghề.
* Nhẹ hơn rất nhiều do bản chất chỉ là 1 file script Python 3.
* Bảo mật hoàn toàn thông tin MyBK bằng thuật toán mã hoá AES 256-bit và mật khẩu cấp 2.
* Mã nguồn mở hoàn toàn để mọi người có thể kiểm tra và có thể học hỏi.

## Cách cài đặt và chạy mã nguồn
Giả định bạn biết cách cài [Python 3](https://www.python.org/) và [di chuyển trong Command Prompt](https://gocinfo.com/tim-hieu-command-prompt-cac-lenh-cmd-thong-dung-tren-windows-part-1.html#1-Lenh-cd-di-chuyen-den-mot-vi-tri-thu-muc-bat-ki) 

1. `cd` tới thư mục bạn download file `main.py` về
2. Cài dependency bằng `pip install -r requirements.txt`
3. Chạy main.py bằng `python main.py` và làm theo hướng dẫn

## Building trên Windows
1. `pip install pyinstaller`
2. `pyinstaller --onefile main.py`
3. Chờ để compile, file trong folder `dist`


## FAQ
### Hỗ trợ iOS?
Nope, app không, và sẽ không bao giờ hỗ trợ iOS vì chi phí ban đầu rất lớn: [100$/năm cho tài khoản Apple của lập trình viên](https://developer.apple.com/support/compare-memberships/) và PC/laptop Apple. Hackintosh? Không. Chỉ đơn giản là không.
### APK/EXE standalone?
Sẽ có trong tương lai gần, nhưng kênh cập nhật sẽ không thông qua Google Play mà sẽ tiếp tục là GitHub vì Google yêu cầu 25$ phí đăng ký và độ trễ giữa đăng update-phân phối update. Nếu tôi cập nhật bản sửa lỗi, tôi muốn mọi người có thể nhận được nó sớm nhất.
### "Nhưng mà app thâm nhập MyBK!!1!"
*NhƯnG mÀ aPp ThÂm NhẬp MyBk!!1!*. Trong mã nguồn tôi từ line 240 tới line 277 là cách mà trình duyệt gửi/nhận thông tin từ máy chủ nhà trường. Nếu bạn muốn thì tự mở Developer Tools của trình duyệt lên và thao tác lại các bước từ đăng nhập Cổng Thông tin Sinh Viên qua SSO tới lấy thời khoá biểu. Nhớ kiểm tra từ Headers, Params tới Response (và chịu khó đọc JavaScript). 
