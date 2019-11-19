# Built-in libraries
import os
import json
import getpass
import sys
from datetime import datetime, date, time

# External libraries
import requests
from bs4 import BeautifulSoup as BS

# Modules
from modules.cryptography import Cryptography
from modules.display import Display
from modules.notifications import Notifications

# Pre-initialization of modules
Cryptography = Cryptography()
Display = Display()
Notifications = Notifications()

# Functions to avoid code re-use
def exit(message, error_code=1):
    '''
    Print a message and wait for user to press Enter to exit.
    Exit code of choice.
    '''
    print(message)
    input('Bấm Enter để tiếp tục...')
    sys.exit(error_code)

# Welcoming splash screen
Notifications.splash()

# Login to application
if not os.path.exists('credential.json'):
    # Set first run flag
    first_run = True
    Notifications.first_run()

    # Get user's MyBK's ID (doesn't necessarily be correct)
    username = input('Tên MyBK: ')
    password = getpass.getpass('Mật khẩu: ')

    user_credential = json.dumps({'username':username, 'password':password})

    # Set up the 2nd level password to further encrypt user's data
    Notifications.second_pw_setup()
    Notifications.second_pw_note()

    while True:
        try:
            second_pw = getpass.getpass('Mật khẩu cấp hai: ')
            second_pw_2 = getpass.getpass('Nhập lại mật khẩu cấp hai: ')

            assert second_pw == second_pw_2
            # Destroy password confirmation variable to prevent leakage
            second_pw_2 = os.urandom(1)
            break # Break out
        except AssertionError:
            print('Mật khẩu cấp hai được nhập không khớp nhau. Vui lòng thực hiện lại\n')
            continue

    # Encrypt the data
    encryption_result = Cryptography.encrypt(data=user_credential,
                                               password=second_pw)
    print('Mã hóa thành công thông tin MyBK của bạn')
    # Destroy second password and plain text data in memory for security
    second_pw, user_credential= [os.urandom(1) for i in range(2)]

    # Store the encrypted data
    with open('credential.json', 'w') as f:
        json.dump(encryption_result, f)

else:
    first_run = False
    # Load the data in from saved credential
    with open('credential.json') as f:
        data = json.load(f)
        credential = data['encrypted_data']
        nonce, salt, tag = [data['initial_state'][i] for i in ['nonce', 'salt', 'tag']]

    # Attempt to decrypt
    Notifications.second_pw_note()
    while True:
        try:
            second_pw = getpass.getpass("Nhập mật khẩu cấp hai: ")
            user_credential = Cryptography.decrypt(password=second_pw,
                                                   encrypted_data=credential,
                                                   nonce=nonce,
                                                   salt=salt,
                                                   tag=tag)
            # Destroy the correct key
            second_pw = os.urandom(1)
            break
        except ValueError:
            print('Sai mật khẩu cấp hai, không thể giải mã.')

    # Load decrypted data into variables and destroy the decrypted
    username, password = [json.loads(user_credential)[i] for i in ['username', 'password']]
    user_credential = os.urandom(1)

# Preliminary sanity check
if any([i == '' for i in (username, password)]):
    exit('Đã có lỗi xảy ra: Username MyBK hoặc mật khẩu bị trống')

# Create new session to log in
s = requests.Session()
try:
    # Log in to SSO for cookie
    r = s.get('https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/')
    page = BS(r.content, 'html5lib')
    token = (page.find('input', {'name': 'lt'})).attrs['value']
    data = {'username': username, 'password': password, 'lt': token,
            'execution': 'e1s1', '_eventId': 'submit', 'submit': 'Login'}
    s.post('https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/', data=data)
    r = s.get('https://mybk.hcmut.edu.vn/stinfo/lichhoc')

    # Destroy login info after finishing since now we're using cookie
    username, password, data = [os.urandom(1) for i in range(3)]

    # Grabbing the token to get the timetable
    r = s.get('https://mybk.hcmut.edu.vn/stinfo/lichhoc')
    page = BS(r.content, 'html5lib')
    token = page.find('meta', {'name': '_token'}).attrs['content']
    r = s.post('https://mybk.hcmut.edu.vn/stinfo/lichthi/ajax_lichhoc', json={'_token': token})
    timetable = r.json()

    # Destroy the session altogether
    token, r, s, page = [os.urandom(1) for i in range(4)]

    # Cache the data just in case
    cached_file = 'cached_data.json'
    with open(cached_file, 'w') as f:
        json.dump(timetable, f)

except OSError: # Every single fucking error that can happen.
    print('Có lỗi trong quá trình kết nối. Dùng thông tin lưu sẵn... ', end='')
    if not os.path.exists('cache_data.json'):
        print() # Ending the previous print()
        exit('Không tìm thấy file lưu sẵn. Vui lòng kết nối mạng và thử lại')
    else:
        last_updated = os.path.getmtime(cached_file)
        last_updated = datetime.fromtimestamp(last_updated).strftime('%d/%m/%Y')
        print(f'(Cập nhật lần cuối: {last_updated})')
        with open(cached_file) as f:
            timetable = json.load(f)
