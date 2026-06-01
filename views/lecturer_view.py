from tkinter import *
from tkinter import ttk, messagebox
import random
import string
from controllers.controllers import LecturerController, MainController

class LecturerWindow:
    def __init__(self, main_controller):
        self.lecturer_ctr = LecturerController(main_controller)

        self.window = Tk()
        self.window.geometry("1000x650")
        self.window.title("BCSE - Giảng Viên")

        # ==========================================
        # SIDEBAR
        # ==========================================
        self.sidebar = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        Label(self.sidebar, text="Giảng viên", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)
        Button(self.sidebar, text="Dashboard", command=self.show_dashboard, font=("Segoe UI", 11)).pack(fill="x", pady=5)
        Button(self.sidebar, text="Mở điểm danh", command=self.show_attendance, font=("Segoe UI", 11)).pack(fill="x", pady=5)
        Button(self.sidebar, text="Quản lý điểm", command=self.show_grade, font=("Segoe UI", 11)).pack(fill="x", pady=5)
        Button(self.sidebar, text="Track Bài Tập", bg="#e6ccff", command=self.show_assignment, font=("Segoe UI", 11)).pack(fill="x", pady=5)

        self.main_frame = Frame(self.window, bg="#f0f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # ==========================================
        # 1. FRAME DASHBOARD
        # ==========================================
        self.frame_dashboard = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_dashboard, text="Lịch Giảng Dạy & Lớp Phụ Trách", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        self.class_listbox = Listbox(self.frame_dashboard, font=("Segoe UI", 12), width=50, height=15)
        self.class_listbox.pack(anchor="w", pady=10)

        # ==========================================
        # 2. FRAME ĐIỂM DANH
        # ==========================================
        self.frame_attendance = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_attendance, text="Kích hoạt phiên Điểm danh", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        
        Label(self.frame_attendance, text="Mã lớp học phần", font=("Segoe UI", 11, "bold"), bg="#f0f4f8").pack(anchor="w")
        self.entry_att_class = Entry(self.frame_attendance, font=("Segoe UI", 13), width=25)
        self.entry_att_class.pack(pady=(0,15), anchor="w")
        
        Label(self.frame_attendance, text="Mã OTP bảo mật", font=("Segoe UI", 11, "bold"), bg="#f0f4f8").pack(anchor="w")
        
        otp_frame = Frame(self.frame_attendance, bg="#f0f4f8")
        otp_frame.pack(anchor="w", pady=(0,15))
        self.entry_att_token = Entry(otp_frame, font=("Segoe UI", 13), width=15)
        self.entry_att_token.pack(side="left", padx=(0, 10))
        Button(otp_frame, text="Tạo OTP ngẫu nhiên", command=self.generate_otp).pack(side="left")

        Button(self.frame_attendance, text="Mở phiên điểm danh", bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), command=self.handle_open_attendance).pack(anchor="w")
        self.lbl_att_result = Label(self.frame_attendance, text="", bg="#f0f4f8", font=("Segoe UI", 11))
        self.lbl_att_result.pack(pady=10, anchor="w")

        # ==========================================
        # 3. FRAME NHẬP/TÍNH/KHÓA ĐIỂM
        # ==========================================
        self.frame_grade = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_grade, text="Quản lý Điểm số", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        
        input_grade_frame = Frame(self.frame_grade, bg="white", bd=1, relief="solid", padx=15, pady=15)
        input_grade_frame.pack(anchor="w", pady=10, fill="x")
        
        Label(input_grade_frame, text="Mã lớp:", font=("Segoe UI", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.entry_grade_class = Entry(input_grade_frame, font=("Segoe UI", 12), width=15)
        self.entry_grade_class.grid(row=0, column=1, padx=10, pady=5)
        
        Label(input_grade_frame, text="Mã SV:", font=("Segoe UI", 10)).grid(row=0, column=2, sticky="w", pady=5)
        self.entry_student = Entry(input_grade_frame, font=("Segoe UI", 12), width=15)
        self.entry_student.grid(row=0, column=3, padx=10, pady=5)

        Label(input_grade_frame, text="Loại điểm:", font=("Segoe UI", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.cmb_score = StringVar(value="chuyen_can")
        OptionMenu(input_grade_frame, self.cmb_score, "chuyen_can", "giua_ky", "cuoi_ky").grid(row=1, column=1, sticky="w", padx=10, pady=5)
        
        Label(input_grade_frame, text="Điểm số:", font=("Segoe UI", 10)).grid(row=1, column=2, sticky="w", pady=5)
        self.entry_score = Entry(input_grade_frame, font=("Segoe UI", 12), width=15)
        self.entry_score.grid(row=1, column=3, padx=10, pady=5)
        
        Button(input_grade_frame, text="💾 Lưu Điểm", command=self.handle_input_grade).grid(row=2, column=0, columnspan=4, pady=10)
        self.lbl_grade_result = Label(input_grade_frame, text="", bg="white")
        self.lbl_grade_result.grid(row=3, column=0, columnspan=4)

        action_grade_frame = Frame(self.frame_grade, bg="#f0f4f8")
        action_grade_frame.pack(anchor="w", pady=10)
        Button(action_grade_frame, text="📊 Tự động tính Điểm tổng kết", bg="#007bff", fg="white", font=("Segoe UI", 11), command=self.calculate_final).pack(side="left", padx=(0, 10))
        Button(action_grade_frame, text="🔒 Khóa điểm lớp này", bg="red", fg="white", font=("Segoe UI", 11), command=self.lock_grades).pack(side="left")

        # ==========================================
        # 4. FRAME TRACK TIẾN ĐỘ BÀI TẬP
        # ==========================================
        self.frame_assignment = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_assignment, text="Theo dõi Tiến độ & Nhắc nhở", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        
        tool_hw_frame = Frame(self.frame_assignment, bg="#f0f4f8")
        tool_hw_frame.pack(fill="x", pady=5)
        Button(tool_hw_frame, text="🔄 Tải danh sách nộp bài", command=self.load_assignments).pack(side="left", padx=5)
        Button(tool_hw_frame, text="🔔 Gửi thông báo nhắc nộp bài (Quá hạn)", bg="#ffc107", font=("Segoe UI", 10, "bold"), command=self.send_reminder).pack(side="right", padx=5)

        cols_hw = ('uid', 'name', 'status', 'time')
        self.tree_hw = ttk.Treeview(self.frame_assignment, columns=cols_hw, show='headings', height=12)
        self.tree_hw.heading('uid', text='Mã SV')
        self.tree_hw.heading('name', text='Họ và Tên')
        self.tree_hw.heading('status', text='Trạng thái')
        self.tree_hw.heading('time', text='Thời gian nộp')
        
        self.tree_hw.column('uid', width=100, anchor='center')
        self.tree_hw.column('name', width=200)
        self.tree_hw.column('status', width=150, anchor='center')
        self.tree_hw.column('time', width=150, anchor='center')
        self.tree_hw.pack(fill="both", expand=True, pady=10)

        self.show_dashboard()
        self.window.mainloop()

    # ==========================================
    # CÁC HÀM ĐIỀU HƯỚNG
    # ==========================================
    def hide_all_frames(self):
        self.frame_dashboard.pack_forget()
        self.frame_attendance.pack_forget()
        self.frame_grade.pack_forget()
        self.frame_assignment.pack_forget()

    def show_dashboard(self):
        self.hide_all_frames()
        self.frame_dashboard.pack(fill="both", expand=True)
        self.class_listbox.delete(0, END)
        classes = self.lecturer_ctr.get_assigned_classes()
        if classes:
            for c in classes:
                self.class_listbox.insert(END, f"{c['class_id']} - {c['course_id']}")
        else:
            self.class_listbox.insert(END, "Chưa có lớp nào được phân công.")

    def show_attendance(self):
        self.hide_all_frames()
        self.frame_attendance.pack(fill="both", expand=True)

    def show_grade(self):
        self.hide_all_frames()
        self.frame_grade.pack(fill="both", expand=True)

    def show_assignment(self):
        self.hide_all_frames()
        self.frame_assignment.pack(fill="both", expand=True)

    # ==========================================
    # CÁC HÀM XỬ LÝ SỰ KIỆN LÕI
    # ==========================================
    def generate_otp(self):
        otp = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        self.entry_att_token.delete(0, END)
        self.entry_att_token.insert(0, otp)

    def handle_open_attendance(self):
        class_id = self.entry_att_class.get().strip()
        token = self.entry_att_token.get().strip()
        if not class_id or not token:
            self.lbl_att_result.config(text="Vui lòng nhập mã lớp và OTP.", fg="red")
            return
        success, message = self.lecturer_ctr.open_attendance(class_id, token)
        self.lbl_att_result.config(text=message, fg="green" if success else "red")

    def handle_input_grade(self):
        class_id = self.entry_grade_class.get().strip()
        student_id = self.entry_student.get().strip()
        score_type = self.cmb_score.get()
        try:
            value = float(self.entry_score.get())
        except ValueError:
            self.lbl_grade_result.config(text="Điểm phải là một con số.", fg="red")
            return
        success, message = self.lecturer_ctr.input_grade(class_id, student_id, score_type, value)
        self.lbl_grade_result.config(text=message, fg="green" if success else "red")

    def calculate_final(self):
        class_id = self.entry_grade_class.get().strip()
        if not class_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã lớp để hệ thống tính điểm tổng kết!")
            return
            
        success, msg = self.lecturer_ctr.calculate_final_grades(class_id)
        if success: messagebox.showinfo("Hoàn tất", msg)
        else: messagebox.showerror("Lỗi", msg)

    def lock_grades(self):
        class_id = self.entry_grade_class.get().strip()
        if not class_id:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã lớp cần khóa điểm!")
            return
            
        confirm = messagebox.askyesno("Khóa điểm", f"Bạn có chắc muốn KHÓA ĐIỂM lớp {class_id} không?\nSau khi khóa, giảng viên sẽ KHÔNG THỂ sửa điểm được nữa!")
        if confirm:
            success, msg = self.lecturer_ctr.lock_class_grades(class_id)
            if success: messagebox.showinfo("Thành công", msg)
            else: messagebox.showerror("Lỗi", msg)

    def load_assignments(self):
        for row in self.tree_hw.get_children(): self.tree_hw.delete(row)
        
        data = self.lecturer_ctr.get_assignments()
        if not data:
            messagebox.showinfo("Trống", "Chưa có bài tập nào được giao trên hệ thống.")
            return
            
        for item in data:
            self.tree_hw.insert('', 'end', values=(item['uid'], item['name'], item['status'], item['time']))

    def send_reminder(self):
        success, msg = self.lecturer_ctr.send_assignment_reminders()
        messagebox.showinfo("Trạng thái Nhắc nhở", msg)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = None
    LecturerWindow(fake_ctrl)