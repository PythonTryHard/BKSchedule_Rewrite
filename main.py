# Thư viện built-in
import os  # Xử lý tác vụ liên quan hệ điều hành
import json  # Xử lý JSON
import getpass  # Nhập password không lộ
from base64 import b64encode, b64decode  # Xử lý dữ liệu encode dạng Base64
import sys  # Xử lý ngừng phần mềm
from datetime import date  # Các tác vụ liên quan đến ngày
import datetime

# Thư viện bên thứ 3
from Crypto.Cipher import AES  # Các tác vụ liên quan mã hoá AES
import requests  # Xử lý yêu cầu mạng
from bs4 import BeautifulSoup as BS  # Xử lý dữ liệu HTML
from Crypto.Protocol.KDF import PBKDF2  # Hash

# Các function để đỡ tốn thời gian
def print_period(period):
    print('-' * (width // 2))
    print(f"Giờ học: [{period['giobd']}-{period['giokt']}] | Phòng [{period['phong1']}] | Cơ sở [{period['macoso']}]")
    print(f"Môn: [{period['ma_mh']} - {period['ma_nhom']}] {period['ten_mh'].strip()}")
    return


def iso_year_start(iso_year):
    """The gregorian calendar date of the first day of the given ISO year"""
    fourth_jan = datetime.date(iso_year, 1, 4)
    delta = datetime.timedelta(fourth_jan.isoweekday() - 1)
    return fourth_jan - delta


def iso_to_gregorian(iso_year, iso_week, iso_day):
    """Gregorian calendar date for the given ISO year, week and day"""
    year_start = iso_year_start(iso_year)
    return year_start + datetime.timedelta(days=iso_day - 1, weeks=iso_week - 1)


# Splash screen chào mừng
print(
'''
0------------------------0
|                        |
|   BKSchedule Rewrite   |
|   Copyright (C) 2019   |
|      GNU GPL v3.0      |
|                        |
|  Coder: PythonTryHard  |
|  Lang : Python 3       |
|  Ver  : v1.0           |
|                        |
|  Phần mềm open-source  |
|                        |
| Vì sự tiện lợi của bạn |
|  không phải là thứ để  |
|       bị tước đi       |
0------------------------0
'''
)
###############################################################################
# Khởi động
# Đăng nhập ứng dụng
if not os.path.exists('credential.json'):
    # Thông tin đăng nhập MyBK
    print('Khai báo tài khoản MyBK lần đầu, và chỉ lần đầu. ', 'Lưu ý: Nhập sai quá 3 lần tài khoản sẽ bị khoá')
    username = input('Tên MyBK: ')
    password = getpass.getpass('Mật khẩu: ')
    # Đăng nhập thử để bảo đảm đúng tài khoản
    s = requests.Session()
    r = s.get('https://sso.hcmut.edu.vn/cas/login?locale=en')
    page = BS(r.content, 'html5lib')
    token = (page.find('input', {'name': 'lt'})).attrs['value']
    data = {
        'username': username,
        'password': password,
        'lt': token,
        'execution': 'e1s1',
        '_eventId': 'submit',
        'submit': 'Login',
    }
    r = s.post('https://sso.hcmut.edu.vn/cas/login', data=data)
    page = BS(r.content, 'html5lib')
    if page.find('div', {'class': 'errors'}):
        input('Sai thông tin MyBK, vui lòng chạy lại chương trình.')
        sys.exit(1)
    # Mật khẩu cấp hai (MK2) để mã hoá thông tin đăng nhập MyBK
    print('*' * 20, '\nLƯU Ý: VUI LÒNG THIẾT LẬP MẬT KHẨU CẤP HAI ĐỂ BẢO VỆ THÔNG TIN TÀI KHOẢN MYBK LƯU TRÊN MÁY')
    print('LƯU Ý: MẬT KHẨU CẤP HAI TỪ 8-16 KÝ TỰ ĐỂ TRÁNH TẤN CÔNG BRUTE-FORCE')
    second_level_password_1 = getpass.getpass('Mật khẩu cấp hai: ')
    second_level_password_2 = getpass.getpass('Nhập lại mật khẩu cấp hai: ')

    # Kiểm tra khớp MK2 và điều kiện độ dài trên 10 ký tự
    second_level_password_match = second_level_password_1 == second_level_password_2
    if second_level_password_match:
        if len(second_level_password_2) in range(8, 16 + 1):
            print('Đang mã hoá thông tin MyBK của bạn...', end='')
            # Tạo salt cho mật khẩu với byte-length = độ dài MK2 * 3
            salt = os.urandom(len(second_level_password_2) * 3)

            # Hash MK2 bằng PBKDF2-HMAC và hash SHA-512, 10000 vòng lặp vì bảo mật
            key = PBKDF2(second_level_password_2, salt, dkLen=32)

            # Mã hoá ID MyBK bằng AES và MK2
            cipher = AES.new(key=key, mode=AES.MODE_EAX)

            credential_string = str.encode(json.dumps(str({"username": username, "password": password})))

            encrypted_credential, tag = cipher.encrypt_and_digest(credential_string)

            # Dịch dữ liệu về Base64
            encrypted_credential = b64encode(encrypted_credential).decode()
            tag = b64encode(tag).decode()
            salt = b64encode(salt).decode()
            nonce = b64encode(cipher.nonce).decode()

            # Ghi file lưu dữ liệu
            with open('credential.json', 'w+') as f:
                data = {'credential': encrypted_credential, 'tag': tag, 'salt': salt, 'nonce': nonce}
                json.dump(data, indent=4, fp=f)
            print('Xong.')
            print('*' * 20)
        else:
            input('Độ dài mật khẩu không khớp yêu cầu. vui lòng chạy lại chương trình')
            sys.exit(1)
    else:
        input('Mật khẩu cấp hai được nhập không khớp nhau. Vui lòng chạy lại chương trình.')
        sys.exit(1)
else:  # File 'credential.json' tồn tại
    print('Chào mừng quay trở lại!\n')
    with open('credential.json', 'rb') as f:
        # Nạp file JSON vào
        data = json.load(f)
        # Kéo dữ liệu ra và decode từ Base64
        credential = b64decode(data['credential'])
        salt = b64decode(data['salt'])
        tag = b64decode(data['tag'])
        nonce = b64decode(data['nonce'])

        # Kiểm tra MK2
        attempt_counter = 1
        while True:
            password_input = getpass.getpass('Vui lòng nhập mật khẩu cấp hai: ')
            password_input_hash = PBKDF2(password_input, salt, dkLen=32)
            password_input = os.urandom(128)
            # Giải mã
            cipher = AES.new(key=password_input_hash, mode=AES.MODE_EAX, nonce=nonce)
            try:
                credential = cipher.decrypt_and_verify(credential, tag)
            except ValueError:
                print('*' * 20, '\nMật khẩu cấp hai 2 sai.')
                continue
            credential = json.loads(str(credential)[3:-2].replace('\\\'', '"'))
            username = credential['username']
            password = credential['password']
            
            # Huỷ dữ liệu JSON đã giải mã
            credential, data = [os.urandom(128) for i in range(2)] 
            
            break
###############################################################################
# Kiểm tra trước phòng ngừa
if username == '' or password == '':
    print('Đã có lỗi xảy ra: Username MyBK hoặc mật khẩu bị trống. Vui lòng xoá file credential.json và thử lại')
    sys.exit(1)

# Thời khoá biểu
print('Đang tìm dữ liệu, vui lòng chờ...')
# Khởi động session
s = requests.Session()
# Lấy OTP từ trang đăng nhập trung tâm
r = s.get('https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/')
page = BS(r.content, 'html5lib')
token = (page.find('input', {'name': 'lt'})).attrs['value']
# Đăng nhập vào hệ thống và lợi dụng redirect để đỡ tốn công
data = {
    'username': username,
    'password': password,
    'lt': token,
    'execution': 'e1s1',
    '_eventId': 'submit',
    'submit': 'Login',
}
s.post('https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/', data=data)

# Huỷ dữ liệu đăng nhập ngay sau khi đăng nhập
username, password, data  = [os.urandom(128) for i in range(3)]

# Cập nhật header yêu cầu. NOTE: CHƯƠNG TRÌNH SẼ KHÔNG CHẠY NẾU KHÔNG CẬP NHẬT
s.headers.update({'X-CSRF-TOKEN': token, 'X-Requested-With': 'XMLHttpRequest'})

# Lấy OTP cho thời khoá biểu
r = s.get('https://mybk.hcmut.edu.vn/stinfo/lichhoc')
page = BS(r.content, 'html5lib')
token = page.find('meta', {'name': '_token'}).attrs['content']

# Lấy thời khoá biểu (JSON)
r = s.post('https://mybk.hcmut.edu.vn/stinfo/lichthi/ajax_lichhoc', json={'_token': token})
timetable = r.json()

# Huỷ token 
token, r, s, page = [os.urandom(128) for i in range(4)]
###############################################################################
# Trả về thông tin cho người dùng
# Tính thông tin ngày và tuần học
today = date.today()

week_number = today.isocalendar()[1]
days = {
    1: ('2', 'Thứ Hai'),
    2: ('3', 'Thứ Ba'),
    3: ('4', 'Thứ Tư'),
    4: ('5', 'Thứ Năm'),
    5: ('6', 'Thứ Sáu'),
    6: ('7', 'Thứ Bảy'),
    7: ('CN', "Chủ Nhật"),
}
day_number = days[today.isocalendar()[2]]
date = today.strftime('%d/%m/%Y')

print(f'\nHôm này ngày {date}, tuần học {week_number}')

# Rút TKB ra khỏi mớ hỗn độn
print(f'\nTìm thấy {len(timetable)} thời khoá biểu: ', end='')
if len(timetable) != 1:
    print()  # Chuyển cursor sang new line
    for i in timetable:
        print(f"{timetable.index(i) + 1 :_>2} {i['ten_hocky']}")
    choice = int(input('Chọn thời khoá biểu để kiểm tra (Bấm Enter để chọn số 1): ') or 1) - 1
    timetable = timetable[choice][0]['tkb']
else:
    print(timetable[0]['ten_hocky'])
    timetable = timetable[0]['tkb']

# Vòng lặp chính
while True:
    # Lựa chọn chức năng:
    print('\nChọn chức năng:' 
          '\n1 Xem thời khoá biểu hôm nay (mặc định)'
          '\n2 Xem thời khoá biểu tuần này'
          '\nq Thoát chương trình')
    menu_choice = (input('> ') or "1")

    # Xử lý theo chức năng
    width, _ = os.get_terminal_size()
    
    # Xem hôm nay
    if menu_choice == '1':
        # Tìm tất cả những môn học ngày hôm nay và tuần này
        match = []
        for i in timetable:
            if (str(week_number) in i['tuan_hoc']) and (day_number[0] == str(i['thu1'])):
                match.append(i)

        # In ra
        if len(match) != 0:
            print(f'\nThời khoá biểu hôm nay ({date})')
            for i in match:
                print_period(i)
            print('-' * (width // 2))
        else:  # Phỏng ngừa khi nghỉ
            print('Không học hôm nay, cẩn thận nếu hôm nay có lịch nghỉ/học bù/thi mà không biết')
    
    # Xem tuần này
    elif menu_choice == '2':
        print(f'Thời khoá biểu tuần {week_number}')
        result = {}
        # Kiểm tra các môn hoc xem tuần này có học hay không và học thứ mấy
        for day in days:
            match = []
            for i in timetable:
                if (str(week_number) in i['tuan_hoc']) and (days[day][0] == str(i['thu1'])):
                    match.append(i)
            result[day] = match
        # Hiển thị
        for day in result:
            print(
                f'\n{days[day][1]} ({(iso_to_gregorian(today.isocalendar()[0], week_number, day)).strftime("%d/%m/%Y")})'
            )
            if len(result[day]) != 0:
                for i in result[day]:
                    print_period(i)
                print('-' * (width // 2))
            else:
                print('-' * (width // 2))
                print('Không có gì cả')
                print('-' * (width // 2))
    
    #Thoát ra êm thấm
    elif menu_choice.lower() == 'q':
        sys.exit(0)
