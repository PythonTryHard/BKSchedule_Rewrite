# BKSchedule Rewrite - Viết bởi SV Bách Khoa cho SV Bách Khoa
Vì gần đây app `BKSchedule` sập, `BKSchedule Rewrite` ra đời. 

Phần mềm nguồn mở theo bản quyền GNU GPL v3.0

## Tính năng
* Thời gian tìm thời khoá biểu nhanh (~5 giây) nhờ bỏ qua các bước load hình ảnh, JS, vv.
* Giao diện tương tác dòng lệnh mặc dù xa lạ nhưng bớt gồ ghề.
* Nhẹ hơn rất nhiều do bản chất chỉ là 1 file script Python 3.
* Bảo mật hoàn toàn thông tin MyBK bằng thuật toán mã hoá AES 256-bit và mật khẩu cấp 2.
* Mã nguồn mở hoàn toàn để mọi người có thể kiểm tra và có thể học hỏi.

## Chạy mã nguồn
Nên chạy trong `venv` để tránh conflict với base.
```shell
pip install -r requirements.txt
python BKSchedule_Rewrite.py
```

## FAQ
### Hỗ trợ iOS?
Nope, app không, và sẽ không bao giờ hỗ trợ iOS vì chi phí ban đầu rất lớn: [100$/năm cho tài khoản Apple của lập trình viên](https://developer.apple.com/support/compare-memberships/) và PC/laptop Apple. Hackintosh? Không. Chỉ đơn giản là không.
### APK/EXE standalone?
Có, nhưng kênh cập nhật sẽ là GitHub. APK hiện đang trong roadmap
### "Nhưng mà app thâm nhập MyBK!!1!"
*NhƯnG mÀ aPp ThÂm NhẬp MyBk!!1!*. Trong mã nguồn tôi từ line 116 tới line 176 là cách mà trình duyệt gửi/nhận thông tin từ máy chủ nhà trường. Nếu bạn muốn thì tự mở Developer Tools của trình duyệt lên và thao tác lại các bước từ đăng nhập Cổng Thông tin Sinh Viên qua SSO tới lấy thời khoá biểu. Nhớ kiểm tra từ Headers, Params tới Response (và chịu khó đọc JavaScript). 
