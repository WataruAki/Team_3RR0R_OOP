
from tkinter import *
from tkinter import messagebox
from controllers import StudentController, MainController

class StudentWindow:
    def __init__(self,main_controller):
        self.student_ctr = StudentController(main_controller)

      
        self.window = Tk()
        self.window.geometry("1920x1080")
        self.window.title("BCSE - Sinh Viên")

        # Sidebar
        self.db_frame = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.db_frame.pack(side="left", fill="y", padx=20, pady=20)
        self.db_frame.pack_propagate(False)

        # Main content
        self.main_frame = Frame(self.window, bg="#f0f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True)

        #Frame Dashboard
        self.frame_dashboard = Frame(self.main_frame, bg="#f0f4f8")
        self.lbl_dashboard = Label(self.frame_dashboard, text="Dashboard", 
                  font=("Segoe UI", 16, "bold"), bg="#f0f4f8")
        self.lbl_dashboard.pack(anchor="w", padx=30, pady=20)
        self.lbl_name = Label(self.frame_dashboard,font=("Segoe UI", 15))
        self.lbl_uid = Label(self.frame_dashboard,font=("Segoe UI", 15))
        self.lbl_gpa = Label(self.frame_dashboard,font=("Segoe UI", 15))
        self.lbl_credit = Label(self.frame_dashboard,font=("Segoe UI", 15))
        
        #Frame Register
        self.frame_register = Frame(self.main_frame, bg="#f0f4f8")
        self.lbl_register = Label(self.frame_register, text="Dang ky mon hoc", 
                  font=("Segoe UI", 16, "bold"), bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_register,text="Mã lớp học phần",font=("Segoe UI",16,'bold')).pack()
        self.entry_class_id = Entry(self.frame_register,font=("Segoe UI",15),width=25)
        self.entry_class_id.pack()
        Button(self.frame_register,text="Đăng ký",command=self.register).pack()

        #Frame Attendance
        self.frame_attendance = Frame(self.main_frame, bg="#f0f4f8")
        self.lbl_attendance = Label(self.frame_attendance, text="Diem danh", 
                  font=("Segoe UI", 16, "bold"), bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_attendance,text="Điểm danh",font=("Segoe UI", 18, "bold")).pack()
        Label(self.frame_attendance,text="Mã lớp học phần:",font=("Segoe UI", 15, "bold")).pack()
        self.entry_att_class = Entry(self.frame_attendance,font=("Segoe UI",15),width=25)
        self.entry_att_class.pack(padx=30,pady=5)
        Label(self.frame_attendance,text="Mã điểm danh:",font=("Segoe UI", 15, "bold")).pack(padx=30)
        self.entry_att_code = Entry(self.frame_attendance,font=("Segoe UI", 15, "bold"),width=30)
        self.entry_att_code.pack(padx=30,pady=5)
        Button(self.frame_attendance,text="Điểm danh",command=self.handle_attendance).pack(padx=30,pady=10)

        Button(self.db_frame, text="Dashboard", command=self.show_dashboard).pack(fill="x", pady=5)
        Button(self.db_frame, text="Đăng ký HP", command=self.show_register).pack(fill="x", pady=5)
        Button(self.db_frame, text="Điểm danh", command=self.show_attendance).pack(fill="x", pady=5)
        self.show_dashboard()
        self.window.mainloop()


# Neu phan nay gay loi thi dua ve comment
    def refresh_dashboard(self):
        info = self.student_ctr.get_dashboard_info()
        profile = info["profile"]
        self.lbl_name.config(text=f"Tên: {profile['name']}")
        self.lbl_uid.config(text=f"MSSV: {profile['uid']}")
        self.lbl_gpa.config(text=f"GPA: {profile['gpa']}")
        self.lbl_credits.config(text=f"Tín chỉ: {profile['credits']}")
        self.lbl_warning.config(text=info["warning"]["message"]) 
        
    def show_dashboard(self):
        self.frame_register.pack_forget()     
        self.frame_attendance.pack_forget()
        #self.refresh_dashboard()
        self.frame_dashboard.pack(fill="both", expand=True)
    
    def register(self):
        class_id = self.entry_class_id.get()
        success, message = self.student_ctr.register_class(class_id)
        if success:
            messagebox.showinfo("Thành công",message)
        else:
            messagebox.showerror("Lỗi",message)
    def show_register(self):
        self.frame_dashboard.pack_forget()
        self.frame_attendance.pack_forget()
        self.frame_register.pack(fill="both", expand=True)


    def handle_attendance(self):
        class_id = self.entry_att_class.get()
        code = self.entry_att_code.get()
        success, message = self.student_ctr.check_in_attendance(class_id,code)
        if success:
            messagebox.showinfo("Thành công",message)
        else:
            messagebox.showerror("Lỗi",message)
    def show_attendance(self):
        self.frame_dashboard.pack_forget()
        self.frame_register.pack_forget()
        self.frame_attendance.pack(fill="both", expand=True)

#Xoa khi co database
if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = None
    StudentWindow(fake_ctrl)