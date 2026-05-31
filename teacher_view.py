from tkinter import *
from tkinter import messagebox
from controllers import LecturerController, MainController

class LecturerWindow:
    def __init__(self, main_controller):
        self.lecturer_ctr = LecturerController(main_controller)

        self.window = Tk()
        self.window.geometry("1920x1080")
        self.window.title("BCSE - Giảng Viên")

        # Sidebar
        self.sidebar = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=(20,0), pady=20)
        self.sidebar.pack_propagate(False)

        Label(self.sidebar, text="Giảng viên", font=("Segoe UI", 13, "bold"), bg="white").pack(pady=(20,30))
        Button(self.sidebar, text="Dashboard", command=self.show_dashboard).pack(fill="x", pady=5)
        Button(self.sidebar, text="Mở điểm danh", command=self.show_attendance).pack(fill="x", pady=5)
        Button(self.sidebar, text="Nhập điểm", command=self.show_grade).pack(fill="x", pady=5)

        # Main content
        self.main_frame = Frame(self.window, bg="#f0f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True)

        # Frame Dashboard
        self.frame_dashboard = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_dashboard, text="Dashboard", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_dashboard, text="Danh sách lớp phụ trách:",
              font=("Segoe UI", 12), bg="#f0f4f8").pack(anchor="w", padx=30)
        self.class_listbox = Listbox(self.frame_dashboard, font=("Segoe UI", 12), width=40, height=15)
        self.class_listbox.pack(padx=30, pady=10, anchor="w")

        # Frame Attendance
        self.frame_attendance = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_attendance, text="Mở điểm danh", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_attendance, text="Mã lớp học phần", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_att_class = Entry(self.frame_attendance, font=("Segoe UI", 13), width=25)
        self.entry_att_class.pack(padx=30, pady=(0,15), anchor="w")
        Label(self.frame_attendance, text="Mã điểm danh", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_att_token = Entry(self.frame_attendance, font=("Segoe UI", 13), width=25)
        self.entry_att_token.pack(padx=30, pady=(0,15), anchor="w")
        Button(self.frame_attendance, text="Mở phiên điểm danh",
               command=self.handle_open_attendance).pack(padx=30, anchor="w")
        self.lbl_att_result = Label(self.frame_attendance, text="", bg="#f0f4f8")
        self.lbl_att_result.pack(padx=30, pady=10, anchor="w")

        # Frame Grade
        self.frame_grade = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_grade, text="Nhập điểm", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_grade, text="Mã lớp", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_grade_class = Entry(self.frame_grade, font=("Segoe UI", 13), width=25)
        self.entry_grade_class.pack(padx=30, pady=(0,10), anchor="w")
        Label(self.frame_grade, text="Mã sinh viên", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_student = Entry(self.frame_grade, font=("Segoe UI", 13), width=25)
        self.entry_student.pack(padx=30, pady=(0,10), anchor="w")
        Label(self.frame_grade, text="Loại điểm", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.cmb_score = StringVar(value="chuyen_can")
        OptionMenu(self.frame_grade, self.cmb_score, "chuyen_can", "giua_ky", "cuoi_ky").pack(
            padx=30, pady=(0,10), anchor="w")
        Label(self.frame_grade, text="Điểm số", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_score = Entry(self.frame_grade, font=("Segoe UI", 13), width=25)
        self.entry_score.pack(padx=30, pady=(0,10), anchor="w")
        Button(self.frame_grade, text="Nhập điểm",
               command=self.handle_input_grade).pack(padx=30, anchor="w")
        self.lbl_grade_result = Label(self.frame_grade, text="", bg="#f0f4f8")
        self.lbl_grade_result.pack(padx=30, pady=10, anchor="w")

        self.show_dashboard()
        self.window.mainloop()

    def handle_open_attendance(self):
        class_id = self.entry_att_class.get().strip()
        token = self.entry_att_token.get().strip()
        if not class_id or not token:
            self.lbl_att_result.config(text="Vui lòng nhập đầy đủ.", fg="red")
            return
        success, message = self.lecturer_ctr.open_attendance(class_id, token)
        color = "green" if success else "red"
        self.lbl_att_result.config(text=message, fg=color)

    def handle_input_grade(self):
        class_id = self.entry_grade_class.get().strip()
        student_id = self.entry_student.get().strip()
        score_type = self.cmb_score.get()
        try:
            value = float(self.entry_score.get())
        except ValueError:
            self.lbl_grade_result.config(text="Điểm phải là số.", fg="red")
            return
        success, message = self.lecturer_ctr.input_grade(class_id, student_id, score_type, value)
        color = "green" if success else "red"
        self.lbl_grade_result.config(text=message, fg=color)

    def show_dashboard(self):
        self.frame_attendance.pack_forget()
        self.frame_grade.pack_forget()
        self.frame_dashboard.pack(fill="both", expand=True)
        # Load danh sách lớp
        self.class_listbox.delete(0, END)
        classes = self.lecturer_ctr.get_assigned_classes()
        if classes:
            for c in classes:
                self.class_listbox.insert(END, f"{c['class_id']} - {c['course_id']}")
        else:
            self.class_listbox.insert(END, "Chưa có lớp nào.")

    def show_attendance(self):
        self.frame_dashboard.pack_forget()
        self.frame_grade.pack_forget()
        self.frame_attendance.pack(fill="both", expand=True)

    def show_grade(self):
        self.frame_dashboard.pack_forget()
        self.frame_attendance.pack_forget()
        self.frame_grade.pack(fill="both", expand=True)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = None
    LecturerWindow(fake_ctrl)