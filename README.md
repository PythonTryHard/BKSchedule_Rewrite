# BKSchedule Rewrite - Viết bởi SV Bách Khoa cho SV Bách Khoa
Vì gần đây app `BKSchedule` sập do nghi vấn bán thông tin SV và "thâm nhập hệ thống", `BKSchedule Rewrite` ra đời với mục đích mang lại sự tiện lợi trong việc tìm thời khoá biểu của sinh viên Đại học Bách Khoa mà vẫn giữ dược sự bảo mật của thông tin đăng nhập hệ thống trường

## Tính năng
* Thời gian tìm thời khoá biểu nhanh (~5 giây) nhờ bỏ qua các bước load hình ảnh, JS, vv.
* Giao diện tương tác dòng lệnh mặc dù xa lạ nhưng bớt gồ ghề.
* Nhẹ hơn rất nhiều do bản chất chỉ là 1 file script Python 3.
* Bảo mật hoàn toàn thông tin MyBK bằng thuật toán mã hoá AES 256-bit và mật khẩu cấp 2.
* Mã nguồn mở hoàn toàn để mọi người có thể kiểm tra và có thể học hỏi.
* Chạy cross-platform Windows và Android.

## Cách cài đặt và chạy mã nguồn
Giả định bạn biết cách cài [Python 3](https://www.python.org/) và [di chuyển trong Command Prompt](https://gocinfo.com/tim-hieu-command-prompt-cac-lenh-cmd-thong-dung-tren-windows-part-1.html#1-Lenh-cd-di-chuyen-den-mot-vi-tri-thu-muc-bat-ki) 

1. `cd` tới thư mục bạn download file `main.py` về
2. Cài dependency bằng `pip install -r requirements.txt`
3. Chạy main.py bằng `python main.py` và làm theo hướng dẫn

## FAQ
### Hỗ trợ iOS?
Nope, app không, và sẽ không bao giờ hỗ trợ iOS vì chi phí ban đầu rất lớn: [100$/năm cho tài khoản Apple của lập trình viên](https://developer.apple.com/support/compare-memberships/) và PC/laptop Apple. Hackintosh? Không. Chỉ đơn giản là không.
### APK/EXE standalone?
Sẽ có trong tương lai gần, nhưng kênh cập nhật sẽ không thông qua Google Play mà sẽ tiếp tục là GitHub vì Google yêu cầu 25$ phí đăng ký và độ trễ giữa đăng update-phân phối update. Nếu tôi cập nhật bản sửa lỗi, tôi muốn mọi người có thể nhận được nó sớm nhất.