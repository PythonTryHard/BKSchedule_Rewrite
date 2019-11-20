# Built-in libraries
import os
import json
import getpass
import sys
from datetime import datetime, date, time, timedelta
import random

# External libraries
import requests
from bs4 import BeautifulSoup as BS

# Modules
from modules.cryptography import Cryptography
from modules.display import Display
from modules.notifications import Notifications
from modules.parser import Parser

# Pre-initialization of modules
Cryptography = Cryptography()
Display = Display()
Notifications = Notifications()
Parser = Parser()

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
            print('Giải mã thành công.')
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

# Grabbing the timetable
cached_file = 'cached_data.json'
try:
    # Grabbing the SSO page
    print('Đăng nhập vào hệ thống...')
    r = s.get('https://sso.hcmut.edu.vn/cas/login?locale=en')
    r = BS(r.content, 'html5lib')
    
    # Grabbing data needed for logging in
    token = (r.find('input', {'name': 'lt'})).attrs['value']
    data = {'username': username,
            'password': password,
            'lt': token, # Token is one-time
            'execution': 'e1s1',
            '_eventId': 'submit',
            'submit': 'Login'}
    
    # Login and check for validity of session
    r = s.post('https://sso.hcmut.edu.vn/cas/login?locale=en', data=data)
    r = BS(r.content, 'html5lib')
    
    # In case of failure...
    if r.find('div', {'class': 'errors'}):
        # Remove the faulty credential file
        os.remove('credential.json')\

        # Deliver the final error message
        error_message = 'Sai thông tin MyBK.'
        if first_run:
            exit(f'{error_message}')
        else: # A rare case, hopefully
            exit(f'{error_message}. Liệu bạn có đổi mật khẩu MyBK?')
    
    # ...or success
    else:
        username, password, data = [os.urandom(1) for i in range(3)]
    
    # Preparation before grabbing the timetable

    s.headers.update({'X-CSRF-TOKEN': token, 
                      'X-Requested-With': 'XMLHttpRequest'})
    
    # This to emulate a user
    print('Giả tạo một tí...')
    s.get('https://sso.hcmut.edu.vn/cas/login?service=http://mybk.hcmut.edu.vn/stinfo/')
    
    # Grabbing the token to get the timetable
    print('Tải thời khóa biểu về...')
    r = s.get('https://mybk.hcmut.edu.vn/stinfo/lichhoc')
    r = BS(r.content, 'html5lib')
    token = r.find('meta', {'name': '_token'}).attrs['content']
    r = s.post('https://mybk.hcmut.edu.vn/stinfo/lichthi/ajax_lichhoc', json={'_token': token})
    
    # Convert the jargon into a proper JSON dict
    timetable = r.json()
    
    # Destroy the session altogether
    token, r, s = [os.urandom(1) for i in range(3)]

    # Cache the data just in case
    with open(cached_file, 'w') as f:
        json.dump(timetable, f)

except OSError: # Every single fucking error that can happen.
    print('Có lỗi trong quá trình kết nối. Dùng thông tin lưu sẵn... ', end='')
    if not os.path.exists(cached_file):
        print() # Ending the previous print()
        exit('Không tìm thấy file lưu sẵn. Vui lòng kết nối mạng và thử lại')
    else:
        last_updated = os.path.getmtime(cached_file)
        last_updated = datetime.fromtimestamp(last_updated).strftime('%d/%m/%Y')
        print(f'(Cập nhật lần cuối: {last_updated})')
        with open(cached_file) as f:
            timetable = json.load(f)

# Print out how many timetables found (Number can be greater than 1)
print(f'\nTìm thấy {len(timetable)} thời khoá biểu: ', end='')

# Handling the case of more than one timetable
# Typical case of junior year or anyone with only one table
if len(timetable) == 1:
    print(timetable[0]['ten_hocky'])
    timetable = timetable[0]['tkb']

# For the more veterans. Never make assumptions of which timtable to use
else: 
    # Terminate the previous line
    print() 
    
    # Printing the name of the table along with a handy index
    for i in timetable:
        print(f"{timetable.index(i) + 1 :_>2} {i['ten_hocky']}")
    
    # Minus one because Python counts from 0 while humans count from 1. Sheesh.
    choice = int(input('Chọn thời khoá biểu để kiểm tra (Bấm Enter để chọn số 1): ') or 1) - 1
    
    # Overwrite the big timetable for ease of handling for developer
    timetable = timetable[choice]['tkb']
