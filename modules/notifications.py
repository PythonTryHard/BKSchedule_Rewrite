class Notifications():
    '''
    Notification prints for the application, tucked away for cleanliness
    '''
    def splash(self):
        print(
            '0------------------------0\n'
            '|                        |\n'
            '|   BKSchedule Rewrite   |\n'
            '|   Copyright (C) 2019   |\n'
            '|      GNU GPL v3.0      |\n'
            '|                        |\n'
            '|  Coder: PythonTryHard  |\n'
            '|  Lang : Python 3       |\n'
            '|  Ver  : v2.0.1         |\n'
            '|                        |\n'
            '|  Phần mềm open-source  |\n'
            '|                        |\n'
            '| Vì sự tiện lợi của bạn |\n'
            '|  không phải là thứ để  |\n'
            '|       bị tước đi       |\n'
            '0------------------------0')
        return

    def password_input_note(self):
        print(
            '*----------------------------------------*\n'
            '| Ghi chú: Mật khẩu được tự che khi nhập |\n'
            '*----------------------------------------*'
        )
        return
        
    def first_run(self):
        print(
            '*------------------------------------------------*\n'
            '|      Khai báo thông tin MyBK lần duy nhất      |\n'
            '| Lưu ý: Nhập sai quá 3 lần tài khoản sẽ bị khóa |\n'
            '*------------------------------------------------*')
        self.password_input_note()
        return

    def second_pw_setup(self):
        print(
            '*-------------------------------------------------*\n'
            '|       VUI LÒNG THIẾT LẬP MẬT KHẨU CẤP HAI       |\n'
            '| ĐỂ BẢO VỆ THÔNG TIN TÀI KHOẢN MYBK LƯU TRÊN MÁY |\n'
            '*-------------------------------------------------*')
        return

    def second_pw_note(self):
        print(
            '*---------------------------------------------------------------------*\n'
            '| Ghi chú: Mật khẩu cấp 2 dùng để đăng nhập ứng dụng, không phải MyBK |\n'
            '*---------------------------------------------------------------------*')
        self.password_input_note()
        return
