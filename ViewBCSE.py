import customtkinter as ctk
from controllers.controllers import MainController

# Import 3 giao diện chính từ thư mục views
from views.acs_view import ASWindow
from views.lecturer_view import LecturerWindow
from views.student_view import StudentWindow

# 💡 ÉP BUỘC MẶC ĐỊNH DARK MODE CHO LOGIN
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")

class LoginWindow:
    def __init__(self):
        self.main_ctrl = MainController()
        
        self.window = ctk.CTk()
        self.window.title("BCSE - Đăng Nhập")
        self.window.geometry("400x320")
        self.window.eval('tk::PlaceWindow . center') # Căn giữa màn hình
        
        # Khung Card bo tròn
        self.card = ctk.CTkFrame(self.window, corner_radius=15)
        self.card.pack(expand=True, fill="both", padx=30, pady=30)
        
        # --- UI ĐĂNG NHẬP ---
        ctk.CTkLabel(self.card, text="BCSE SYSTEM", font=("Segoe UI", 24, "bold"), text_color="#3B82F6").pack(pady=(20, 15))
        
        self.entry_email = ctk.CTkEntry(self.card, placeholder_text="Nhập Email (VD: giaovu@vnu.edu.vn)", font=("Segoe UI", 12), height=40)
        self.entry_email.pack(fill="x", padx=30, pady=10)
        
        self.entry_pwd = ctk.CTkEntry(self.card, placeholder_text="Mật khẩu", show="*", font=("Segoe UI", 12), height=40)
        self.entry_pwd.pack(fill="x", padx=30, pady=5)
        
        self.btn_login = ctk.CTkButton(self.card, text="ĐĂNG NHẬP", font=("Segoe UI", 13, "bold"), height=40, command=self.handle_login)
        self.btn_login.pack(fill="x", padx=30, pady=15)
        
        # Nhãn báo lỗi
        self.lbl_error = ctk.CTkLabel(self.card, text="", text_color="#EF4444", font=("Segoe UI", 11))
        self.lbl_error.pack()
        
        # Tính năng bấm Enter
        self.window.bind('<Return>', self.handle_login)
        
        self.window.mainloop()

    def handle_login(self, event=None):
        email = self.entry_email.get().strip()
        pwd = self.entry_pwd.get().strip()
        
        success, msg, role = self.main_ctrl.login(email, pwd)
        
        if success:
            self.window.destroy() # Tiêu diệt login
            
            # Khởi tạo giao diện theo Role
            if role == 'Staff': ASWindow(self.main_ctrl)
            elif role == 'Lecturer': LecturerWindow(self.main_ctrl)
            elif role == 'Student': StudentWindow(self.main_ctrl)
        else:
            self.lbl_error.configure(text="Email hoặc Mật khẩu không chính xác")

if __name__ == "__main__":
    LoginWindow()