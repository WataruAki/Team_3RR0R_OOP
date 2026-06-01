from tkinter import *
from tkinter import ttk, messagebox, filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers.controllers import AcademicStaffController, MainController

class ASWindow:
    def __init__(self, main_controller):
        self.staff_ctr = AcademicStaffController(main_controller)
        
        self.window = Tk()
        self.window.geometry("1000x650")
        self.window.title("BCSE - Giáo Vụ")

        # Sidebar
        self.db_frame = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.db_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.db_frame.pack_propagate(False)

        Label(self.db_frame, text="Giáo vụ", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)
        
        Button(self.db_frame, text="Quản lý Tài khoản", bg="#e6ccff", font=("Segoe UI", 11, "bold"), command=self.show_crud).pack(fill="x", pady=5)
        Button(self.db_frame, text="Xét học bổng", font=("Segoe UI", 11), command=self.show_scholarship).pack(fill="x", pady=5)
        Button(self.db_frame, text="Thống kê GPA", font=("Segoe UI", 11), command=self.show_statistics).pack(fill="x", pady=5)
        Button(self.db_frame, text="Quản lý Học vụ", bg="#ffcccc", font=("Segoe UI", 11), command=self.show_management).pack(fill="x", pady=5)

        self.main_frame = Frame(self.window, bg="#f4f6f9")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # ==========================================
        # 1. FRAME CRUD TÀI KHOẢN (Tính năng mới)
        # ==========================================
        self.frame_crud = Frame(self.main_frame, bg="#f4f6f9")
        Label(self.frame_crud, text="Quản lý Tài khoản Hệ thống", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        
        form_frame = Frame(self.frame_crud, bg="white", bd=1, relief="solid", padx=15, pady=15)
        form_frame.pack(fill="x", pady=5)
        
        Label(form_frame, text="Mã ID:", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_uid = Entry(form_frame, width=20)
        self.entry_uid.grid(row=0, column=1, padx=10)
        
        Label(form_frame, text="Họ và Tên:", bg="white").grid(row=0, column=2, sticky="w", pady=5)
        self.entry_name = Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=3, padx=10)
        
        Label(form_frame, text="Email:", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_email = Entry(form_frame, width=20)
        self.entry_email.grid(row=1, column=1, padx=10)

        Label(form_frame, text="Mật khẩu:", bg="white").grid(row=1, column=2, sticky="w", pady=5)
        self.entry_pwd = Entry(form_frame, width=30)
        self.entry_pwd.grid(row=1, column=3, padx=10)

        Label(form_frame, text="Vai trò:", bg="white").grid(row=2, column=0, sticky="w", pady=5)
        self.cmb_role = ttk.Combobox(form_frame, values=["Student", "Lecturer", "Staff"], state="readonly", width=17)
        self.cmb_role.set("Student")
        self.cmb_role.grid(row=2, column=1, padx=10)

        btn_frame = Frame(form_frame, bg="white")
        btn_frame.grid(row=3, column=0, columnspan=4, pady=15)
        Button(btn_frame, text="Làm mới", command=self.clear_form).pack(side="left", padx=5)
        Button(btn_frame, text="Thêm (Create)", bg="#28a745", fg="white", command=self.add_user).pack(side="left", padx=5)
        Button(btn_frame, text="Sửa (Update)", bg="#007bff", fg="white", command=self.update_user).pack(side="left", padx=5)
        Button(btn_frame, text="Xóa (Delete)", bg="#dc3545", fg="white", command=self.delete_user).pack(side="left", padx=5)

        cols_crud = ('uid', 'name', 'email', 'role')
        self.tree_crud = ttk.Treeview(self.frame_crud, columns=cols_crud, show='headings', height=10)
        self.tree_crud.heading('uid', text='Mã ID')
        self.tree_crud.heading('name', text='Họ và Tên')
        self.tree_crud.heading('email', text='Email')
        self.tree_crud.heading('role', text='Phân quyền')
        self.tree_crud.column('uid', width=100, anchor='center')
        self.tree_crud.column('role', width=100, anchor='center')
        self.tree_crud.pack(fill="both", expand=True, pady=10)
        self.tree_crud.bind("<ButtonRelease-1>", self.select_user)

        # ==========================================
        # CÁC FRAME CŨ (Giữ nguyên)
        # ==========================================
        self.frame_scholarship = Frame(self.main_frame, bg="#f4f6f9")
        # [Giữ nguyên nội dung Frame Xét Học Bổng...]
        Label(self.frame_scholarship, text="Xét Duyệt Học Bổng", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        frame_input = Frame(self.frame_scholarship, bg="#f4f6f9")
        frame_input.pack(anchor="w", pady=10)
        Label(frame_input, text="Số lượng suất:", font=("Segoe UI", 12), bg="#f4f6f9").pack(side="left")
        self.entry_slots = Entry(frame_input, font=("Segoe UI", 12), width=10)
        self.entry_slots.pack(side="left", padx=10)
        Button(frame_input, text="Chạy Engine", command=self.run_scholarship).pack(side="left")
        self.tree_hb = ttk.Treeview(self.frame_scholarship, columns=('uid', 'name', 'score'), show='headings', height=10)
        self.tree_hb.heading('uid', text='Mã SV')
        self.tree_hb.heading('name', text='Họ và Tên')
        self.tree_hb.heading('score', text='Điểm Xét Tuyển')
        self.tree_hb.pack(fill="both", expand=True, pady=10)

        self.frame_statistics = Frame(self.main_frame, bg="#f4f6f9")
        # [Giữ nguyên nội dung Frame Thống kê...]
        Label(self.frame_statistics, text="Thống kê GPA", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        Button(self.frame_statistics, text="Tải dữ liệu", font=("Segoe UI", 10), command=self.load_data).pack(anchor="w", pady=5)
        self.content_frame = Frame(self.frame_statistics, bg="#f4f6f9")
        self.content_frame.pack(fill="both", expand=True, pady=10)
        self.tree_stat = ttk.Treeview(self.content_frame, columns=('loai', 'so_luong'), show='headings', height=6)
        self.tree_stat.heading('loai', text='Xếp loại')
        self.tree_stat.heading('so_luong', text='Số sinh viên')
        self.tree_stat.pack(side="left", anchor="n", padx=(0, 20))
        self.chart_frame = Frame(self.content_frame, bg="#f4f6f9")
        self.chart_frame.pack(side="left", fill="both", expand=True)

        self.frame_management = Frame(self.main_frame, bg="#f4f6f9")
        # [Giữ nguyên nội dung Frame Quản lý Học vụ...]
        Label(self.frame_management, text="Quản lý Cảnh cáo & Xuất Báo Cáo", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        tool_frame = Frame(self.frame_management, bg="#f4f6f9")
        tool_frame.pack(fill="x", pady=5)
        Button(tool_frame, text="🔄 Tải DS Nguy hiểm", command=self.load_at_risk_students).pack(side="left", padx=5)
        Button(tool_frame, text="⚠️ Phát Cảnh Cáo", bg="orange", command=lambda: self.change_status("Cảnh cáo học vụ")).pack(side="left", padx=5)
        Button(tool_frame, text="⛔ Đình Chỉ Học", bg="red", fg="white", command=lambda: self.change_status("Đình chỉ học")).pack(side="left", padx=5)
        Button(tool_frame, text="⬇️ Xuất Báo Cáo Excel", bg="#28a745", fg="white", command=self.export_excel).pack(side="right", padx=5)
        self.tree_mng = ttk.Treeview(self.frame_management, columns=('uid', 'name', 'gpa', 'att', 'status'), show='headings', height=15)
        self.tree_mng.heading('uid', text='Mã SV')
        self.tree_mng.heading('name', text='Họ và Tên')
        self.tree_mng.heading('gpa', text='GPA')
        self.tree_mng.heading('att', text='Chuyên cần')
        self.tree_mng.heading('status', text='Trạng thái hiện tại')
        self.tree_mng.pack(fill="both", expand=True, pady=10)

        self.show_crud()
        self.window.mainloop()

    # ==========================================
    # ĐIỀU HƯỚNG
    # ==========================================
    def hide_all(self):
        self.frame_crud.pack_forget()
        self.frame_scholarship.pack_forget()
        self.frame_statistics.pack_forget()
        self.frame_management.pack_forget()

    def show_crud(self):
        self.hide_all()
        self.frame_crud.pack(fill="both", expand=True)
        self.load_users()

    def show_scholarship(self):
        self.hide_all()
        self.frame_scholarship.pack(fill="both", expand=True)

    def show_statistics(self):
        self.hide_all()
        self.frame_statistics.pack(fill="both", expand=True)

    def show_management(self):
        self.hide_all()
        self.frame_management.pack(fill="both", expand=True)

    # ==========================================
    # LOGIC CRUD TÀI KHOẢN
    # ==========================================
    def load_users(self):
        for row in self.tree_crud.get_children(): self.tree_crud.delete(row)
        users = self.staff_ctr.get_all_users()
        for u in users: self.tree_crud.insert('', 'end', values=(u['uid'], u['name'], u['email'], u['role']))

    def select_user(self, event):
        selected = self.tree_crud.selection()
        if selected:
            item = self.tree_crud.item(selected[0])['values']
            self.clear_form()
            self.entry_uid.insert(0, item[0])
            self.entry_name.insert(0, item[1])
            self.entry_email.insert(0, item[2])
            self.entry_pwd.insert(0, "******") # Ẩn pass
            self.cmb_role.set(item[3])
            self.entry_uid.config(state="disabled") # Không cho sửa ID

    def clear_form(self):
        self.entry_uid.config(state="normal")
        self.entry_uid.delete(0, END)
        self.entry_name.delete(0, END)
        self.entry_email.delete(0, END)
        self.entry_pwd.delete(0, END)

    def add_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        if not all([uid, name, email, pwd, role]):
            messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!")
            return
        success, msg = self.staff_ctr.create_user(uid, name, email, pwd, role)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.load_users()
            self.clear_form()
        else: messagebox.showerror("Lỗi", msg)

    def update_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        success, msg = self.staff_ctr.update_user(uid, name, email, pwd, role)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.load_users()
        else: messagebox.showerror("Lỗi", msg)

    def delete_user(self):
        uid = self.entry_uid.get()
        if not uid: return
        if messagebox.askyesno("Cảnh báo", "Xóa tài khoản sẽ ảnh hưởng tới dữ liệu điểm/lớp học. Bạn chắc chứ?"):
            success, msg = self.staff_ctr.delete_user(uid)
            if success:
                messagebox.showinfo("Thành công", msg)
                self.load_users()
                self.clear_form()
            else: messagebox.showerror("Lỗi", msg)

    # [GIỮ NGUYÊN CÁC HÀM XỬ LÝ CŨ: load_at_risk_students, change_status, export_excel, run_scholarship, load_data, draw_pie_chart...]
    def load_at_risk_students(self):
        for row in self.tree_mng.get_children(): self.tree_mng.delete(row)
        students = self.staff_ctr.get_at_risk_students()
        for s in students: self.tree_mng.insert('', 'end', values=(s['uid'], s['name'], s['gpa'], s['att'], s['status']))
    
    def change_status(self, new_status):
        selected = self.tree_mng.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Vui lòng click chọn 1 sinh viên trong bảng!")
            return
        item = self.tree_mng.item(selected[0])
        success, msg = self.staff_ctr.update_student_status(str(item['values'][0]), new_status)
        if success:
            messagebox.showinfo("Thành công", msg)
            self.load_at_risk_students()
        else: messagebox.showerror("Lỗi", msg)

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Lưu báo cáo")
        if file_path:
            success, msg = self.staff_ctr.export_report_to_excel(file_path)
            if success: messagebox.showinfo("Hoàn tất", f"{msg}\nĐã lưu tại:\n{file_path}")
            else: messagebox.showerror("Lỗi xuất file", msg)

    def run_scholarship(self):
        for row in self.tree_hb.get_children(): self.tree_hb.delete(row)
        try:
            winners = self.staff_ctr.execute_scholarship_filter(int(self.entry_slots.get()))
            for w in winners: self.tree_hb.insert('', 'end', values=(w['uid'], w['name'], f"{w['score']:.2f}"))
        except ValueError: messagebox.showerror("Lỗi", "Vui lòng nhập một số nguyên!")

    def load_data(self):
        data = self.staff_ctr.load_pie_chart_data()
        if not data: return
        for row in self.tree_stat.get_children(): self.tree_stat.delete(row)
        for k, v in data.items(): self.tree_stat.insert('', 'end', values=(k, v))
        self.draw_pie_chart(data)

    def draw_pie_chart(self, data):
        for widget in self.chart_frame.winfo_children(): widget.destroy()
        labels, sizes = [k for k, v in data.items() if v > 0], [v for k, v in data.items() if v > 0]
        fig = Figure(figsize=(5, 4), dpi=100)
        fig.patch.set_facecolor('#f4f6f9')
        ax = fig.add_subplot(111)
        if not sizes: ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center', va='center')
        else:
            ax.pie(sizes, labels=labels, colors=['#ff9999', '#66b3ff', '#99ff99', '#ffcc99'], autopct='%1.1f%%', startangle=140)
            ax.set_title("Tỉ lệ Học lực Toàn khóa", pad=20, fontweight='bold')
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = type('obj', (object,), {'role': 'Staff'})() 
    ASWindow(fake_ctrl)