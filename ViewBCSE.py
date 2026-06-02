from tkinter import *
from controllers.controllers import MainController

# Import 3 giao diện chính từ thư mục views
from views.acs_view import ASWindow
from views.lecturer_view import LecturerWindow
from views.student_view import StudentWindow

class LoginWindow:
    def __init__(self):
        self.main_ctrl = MainController()
        
        self.window = Tk()
        self.window.title("BCSE - Dang Nhap")
        self.window.geometry("350x250")
        self.window.eval('tk::PlaceWindow . center') # Căn giữa màn hình
        
        # --- UI ĐĂNG NHẬP ---
        Label(self.window, text="Gmail", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=40, pady=(20, 0))
        self.entry_email = Entry(self.window, font=("Segoe UI", 12))
        self.entry_email.pack(fill="x", padx=40, pady=5)
        
        Label(self.window, text="Password", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=40)
        self.entry_pwd = Entry(self.window, font=("Segoe UI", 12), show="*")
        self.entry_pwd.pack(fill="x", padx=40, pady=5)
        
        Button(self.window, text="Sign in", font=("Segoe UI", 11, "bold"), bg="#e0e0e0", command=self.handle_login).pack(fill="x", padx=40, pady=15)
        
        # Nhãn báo lỗi (ẩn đi lúc đầu)
        self.lbl_error = Label(self.window, text="", fg="red", font=("Segoe UI", 9))
        self.lbl_error.pack()
        
        # 💡 THÊM TÍNH NĂNG BẤM ENTER ĐỂ ĐĂNG NHẬP
        self.window.bind('<Return>', self.handle_login)
        
        self.window.mainloop()

    # 💡 Thêm tham số `event=None` để tương thích với cả lệnh Click chuột và lệnh Gõ phím
    def handle_login(self, event=None):
        email = self.entry_email.get().strip()
        pwd = self.entry_pwd.get().strip()
        
        # Gọi hàm login từ Controller
        success, msg, role = self.main_ctrl.login(email, pwd)
        
        if success:
            # TIÊU DIỆT CỬA SỔ ĐĂNG NHẬP
            self.window.destroy()
            
            # ĐIỀU HƯỚNG TỚI CỬA SỔ TƯƠNG ỨNG THEO ROLE
            if role == 'Staff':
                ASWindow(self.main_ctrl)
            elif role == 'Lecturer':
                LecturerWindow(self.main_ctrl)
            elif role == 'Student':
                StudentWindow(self.main_ctrl)
        else:
            # Nếu sai pass, hiện dòng chữ đỏ lên
            self.lbl_error.config(text="Email hoặc Mật khẩu không chính xác")

if __name__ == "__main__":
    LoginWindow()