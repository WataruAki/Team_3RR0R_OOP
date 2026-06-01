from tkinter import *
from tkinter import ttk, messagebox
from controllers.controllers import StudentController, MainController

class StudentWindow:
    def __init__(self, main_controller):
        self.student_ctr = StudentController(main_controller)

        self.window = Tk()
        self.window.geometry("1000x650")
        self.window.title("BCSE - Sinh Viên")

        self.sidebar = Frame(self.window, width=200, bg="#eafaf1", bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=10, pady=10)
        self.sidebar.pack_propagate(False)

        Label(self.sidebar, text="SINH VIÊN", font=("Segoe UI", 16, "bold"), fg="#2ecc71", bg="#eafaf1").pack(pady=20)
        
        btn_style = {"bg": "#2ecc71", "fg": "white", "font": ("Segoe UI", 11, "bold"), "pady": 5}
        Button(self.sidebar, text="Thông báo học vụ", command=self.show_dashboard, **btn_style).pack(fill="x", pady=5, padx=10)
        Button(self.sidebar, text="Nộp bài tập", command=self.show_assignment, **btn_style).pack(fill="x", pady=5, padx=10)
        Button(self.sidebar, text="Đăng ký học phần", command=self.show_register, **btn_style).pack(fill="x", pady=5, padx=10)
        Button(self.sidebar, text="Tra cứu điểm & GPA", command=self.show_grades, **btn_style).pack(fill="x", pady=5, padx=10)
        Button(self.sidebar, text="Điểm danh OTP", command=self.show_attendance, **btn_style).pack(fill="x", pady=5, padx=10)

        self.main_frame = Frame(self.window, bg="#f0f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # 1. DASHBOARD
        self.frame_dashboard = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_dashboard, text="Tổng quan & Thông báo học vụ", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        
        self.info_frame = Frame(self.frame_dashboard, bg="white", bd=1, relief="solid", padx=15, pady=15)
        self.info_frame.pack(fill="x", pady=10)
        self.lbl_profile = Label(self.info_frame, text="Đang tải...", font=("Segoe UI", 12), bg="white")
        self.lbl_profile.pack(anchor="w")
        self.lbl_warning = Label(self.info_frame, text="", font=("Segoe UI", 12, "bold"), bg="white")
        self.lbl_warning.pack(anchor="w", pady=5)

        Label(self.frame_dashboard, text="Hòm thư cảnh báo / Nhắc nhở bài tập:", font=("Segoe UI", 12, "bold"), fg="red", bg="#f0f4f8").pack(anchor="w", pady=5)
        self.list_notis = Listbox(self.frame_dashboard, font=("Segoe UI", 11), fg="red", bg="white", height=10)
        self.list_notis.pack(fill="both", expand=True)

        # 2. BÀI TẬP
        self.frame_assignment = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_assignment, text="Nộp bài tập / Chấm điểm", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        
        cols_hw = ('id', 'class', 'status', 'time')
        self.tree_hw = ttk.Treeview(self.frame_assignment, columns=cols_hw, show='headings', height=8)
        self.tree_hw.heading('id', text='ID')
        self.tree_hw.heading('class', text='Mã Lớp')
        self.tree_hw.heading('status', text='Trạng thái')
        self.tree_hw.heading('time', text='Thời gian nộp')
        self.tree_hw.column('id', width=50, anchor='center')
        self.tree_hw.column('class', width=150, anchor='center')
        self.tree_hw.column('status', width=150, anchor='center')
        self.tree_hw.column('time', width=200, anchor='center')
        self.tree_hw.pack(fill="both", pady=10)
        Button(self.frame_assignment, text="📤 Nộp bài tập đã chọn", font=("Segoe UI", 11, "bold"), bg="#3498db", fg="white", command=self.submit_hw).pack(pady=5)

        # 3. ĐĂNG KÝ
        self.frame_register = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_register, text="Đăng ký học phần", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        Label(self.frame_register, text="Mã lớp học phần:", font=("Segoe UI",12), bg="#f0f4f8").pack(pady=5)
        self.entry_class_id = Entry(self.frame_register, font=("Segoe UI",14), width=25)
        self.entry_class_id.pack(pady=5)
        Button(self.frame_register, text="Gửi Đăng Ký", command=self.register, font=("Segoe UI",11)).pack(pady=10)

        # 4. TRA CỨU ĐIỂM
        self.frame_grades = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_grades, text="Tra cứu điểm, GPA, Lịch thi", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        self.lbl_scholarship = Label(self.frame_grades, text="", font=("Segoe UI", 12, "bold"), bg="#f0f4f8")
        self.lbl_scholarship.pack(anchor="w", pady=5)

        cols_gr = ('class', 'cc', 'gk', 'ck', 'tong', 'he4')
        self.tree_gr = ttk.Treeview(self.frame_grades, columns=cols_gr, show='headings', height=10)
        self.tree_gr.heading('class', text='Mã Lớp')
        self.tree_gr.heading('cc', text='Chuyên cần')
        self.tree_gr.heading('gk', text='Giữa kỳ')
        self.tree_gr.heading('ck', text='Cuối kỳ')
        self.tree_gr.heading('tong', text='Tổng kết (Hệ 10)')
        self.tree_gr.heading('he4', text='Hệ 4')
        for col in cols_gr: self.tree_gr.column(col, width=100, anchor='center')
        self.tree_gr.pack(fill="both", expand=True, pady=10)

        # 5. ĐIỂM DANH OTP
        self.frame_attendance = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_attendance, text="Điểm danh OTP", font=("Segoe UI", 18, "bold"), bg="#f0f4f8").pack(anchor="w", pady=10)
        Label(self.frame_attendance, text="Mã lớp học phần:", font=("Segoe UI", 12), bg="#f0f4f8").pack(pady=5)
        self.entry_att_class = Entry(self.frame_attendance, font=("Segoe UI",14), width=25)
        self.entry_att_class.pack(pady=5)
        Label(self.frame_attendance, text="Mã xác nhận bảo mật:", font=("Segoe UI", 12), bg="#f0f4f8").pack(pady=5)
        self.entry_att_code = Entry(self.frame_attendance, font=("Segoe UI", 14, "bold"), width=25)
        self.entry_att_code.pack(pady=5)
        Button(self.frame_attendance, text="Check-in", bg="#28a745", fg="white", font=("Segoe UI",11,"bold"), command=self.handle_attendance).pack(pady=15)

        self.show_dashboard()
        self.window.mainloop()

    def hide_all(self):
        self.frame_dashboard.pack_forget()
        self.frame_assignment.pack_forget()
        self.frame_register.pack_forget()
        self.frame_grades.pack_forget()
        self.frame_attendance.pack_forget()

    def show_dashboard(self):
        self.hide_all()
        self.frame_dashboard.pack(fill="both", expand=True)
        info = self.student_ctr.get_dashboard_info()
        if info and "profile" in info:
            p = info["profile"]
            self.lbl_profile.config(text=f"👨‍🎓 Họ tên: {p['name']}  |  🆔 UID: {p['uid']}  |  📈 GPA: {p['gpa']}  |  📚 Tín chỉ: {p['credits']}")
            if info["warning"]["is_warned"]: self.lbl_warning.config(text=f"⚠️ {info['warning']['message']}", fg="red")
            else: self.lbl_warning.config(text=f"✅ {info['warning']['message']}", fg="green")
        
        self.list_notis.delete(0, END)
        notis = self.student_ctr.get_notifications()
        if not notis: self.list_notis.insert(END, "Không có thông báo nhắc nhở nào.")
        for n in notis: self.list_notis.insert(END, f"📢 [{n['time']}] {n['msg']}")

    def show_assignment(self):
        self.hide_all()
        self.frame_assignment.pack(fill="both", expand=True)
        for row in self.tree_hw.get_children(): self.tree_hw.delete(row)
        for h in self.student_ctr.get_assignments(): 
            self.tree_hw.insert('', 'end', values=(h['id'], h['class_id'], h['status'], h['time'] or "---"))

    def show_register(self):
        self.hide_all()
        self.frame_register.pack(fill="both", expand=True)

    def show_grades(self):
        self.hide_all()
        self.frame_grades.pack(fill="both", expand=True)
        for row in self.tree_gr.get_children(): self.tree_gr.delete(row)
        for g in self.student_ctr.get_detailed_grades(): 
            self.tree_gr.insert('', 'end', values=(g['class_id'], g['cc'], g['gk'], g['ck'], g['tong'] or "---", g['he4'] or "---"))
        
        info = self.student_ctr.get_dashboard_info()
        if info and "profile" in info:
            p = info["profile"]
            if p['credits'] >= 18 and p['gpa'] >= 3.2: self.lbl_scholarship.config(text="🎉 Đủ điều kiện xét duyệt học bổng kỳ này!", fg="#28a745")
            else: self.lbl_scholarship.config(text="❌ Chưa đủ điều kiện xét học bổng.", fg="red")

    def show_attendance(self):
        self.hide_all()
        self.frame_attendance.pack(fill="both", expand=True)

    def submit_hw(self):
        selected = self.tree_hw.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 bài tập để nộp!")
            return
        hw_id = self.tree_hw.item(selected[0])['values'][0]
        success, msg = self.student_ctr.submit_assignment(int(hw_id))
        if success:
            messagebox.showinfo("Thành công", msg)
            self.show_assignment()
        else: messagebox.showerror("Lỗi", msg)

    def register(self):
        class_id = self.entry_class_id.get().strip()
        success, msg = self.student_ctr.register_class(class_id)
        if success: messagebox.showinfo("Thành công", msg)
        else: messagebox.showerror("Bị chặn", msg)

    def handle_attendance(self):
        class_id, code = self.entry_att_class.get().strip(), self.entry_att_code.get().strip()
        success, msg = self.student_ctr.check_in_attendance(class_id, code)
        if success: messagebox.showinfo("Thành công", msg)
        else: messagebox.showerror("Lỗi Điểm Danh", msg)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = None
    StudentWindow(fake_ctrl)