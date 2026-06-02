from tkinter import *
from tkinter import ttk, messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers.controllers import AcademicStaffController, MainController

class ASWindow:
    def __init__(self, main_controller):
        self.staff_ctr = AcademicStaffController(main_controller)
        self.window = Tk()
        self.window.geometry("1000x650")
        self.window.title("BCSE - Giáo Vụ")

        # ==========================================
        # SIDEBAR
        # ==========================================
        self.db_frame = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.db_frame.pack(side="left", fill="y", padx=10, pady=10)
        self.db_frame.pack_propagate(False)

        Label(self.db_frame, text="Giáo vụ", font=("Segoe UI", 16, "bold"), bg="white").pack(pady=20)
        Button(self.db_frame, text="Quản lý Hệ thống", bg="#e6ccff", font=("Segoe UI", 11, "bold"), command=self.show_crud).pack(fill="x", pady=5)
        Button(self.db_frame, text="Xét học bổng", font=("Segoe UI", 11), command=self.show_scholarship).pack(fill="x", pady=5)
        Button(self.db_frame, text="Thống kê GPA", font=("Segoe UI", 11), command=self.show_statistics).pack(fill="x", pady=5)
        Button(self.db_frame, text="Quản lý Học vụ", bg="#ffcccc", font=("Segoe UI", 11), command=self.show_management).pack(fill="x", pady=5)

        self.main_frame = Frame(self.window, bg="#f4f6f9")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Khởi tạo các Frame
        self.frame_crud = Frame(self.main_frame, bg="#f4f6f9")
        self.frame_scholarship = Frame(self.main_frame, bg="#f4f6f9")
        self.frame_statistics = Frame(self.main_frame, bg="#f4f6f9")
        self.frame_management = Frame(self.main_frame, bg="#f4f6f9")
        
        # ==========================================
        # 1. GIAO DIỆN: CRUD TÀI KHOẢN & HỌC PHẦN
        # ==========================================
        form_frame = Frame(self.frame_crud, bg="white", bd=1, relief="solid", padx=15, pady=15)
        form_frame.pack(fill="x", pady=5)
        
        Label(form_frame, text="Mã ID:", bg="white").grid(row=0, column=0, pady=5, sticky="w"); self.entry_uid = Entry(form_frame, width=20); self.entry_uid.grid(row=0, column=1, padx=10)
        Label(form_frame, text="Họ Tên:", bg="white").grid(row=0, column=2, pady=5, sticky="w"); self.entry_name = Entry(form_frame, width=30); self.entry_name.grid(row=0, column=3, padx=10)
        Label(form_frame, text="Email:", bg="white").grid(row=1, column=0, pady=5, sticky="w"); self.entry_email = Entry(form_frame, width=20); self.entry_email.grid(row=1, column=1, padx=10)
        Label(form_frame, text="Pass (8 ký tự):", bg="white").grid(row=1, column=2, pady=5, sticky="w"); self.entry_pwd = Entry(form_frame, width=30); self.entry_pwd.grid(row=1, column=3, padx=10)
        Label(form_frame, text="Vai trò:", bg="white").grid(row=2, column=0, pady=5, sticky="w"); self.cmb_role = ttk.Combobox(form_frame, values=["Student", "Lecturer", "Staff"], state="readonly", width=17); self.cmb_role.set("Student"); self.cmb_role.grid(row=2, column=1, padx=10)
        
        btn_f = Frame(form_frame, bg="white"); btn_f.grid(row=3, column=0, columnspan=4, pady=10)
        Button(btn_f, text="Làm mới", command=self.clear_form).pack(side="left", padx=5)
        Button(btn_f, text="Thêm (Create)", bg="#28a745", fg="white", command=self.add_user).pack(side="left", padx=5)
        Button(btn_f, text="Sửa (Update)", bg="#007bff", fg="white", command=self.update_user).pack(side="left", padx=5)
        Button(btn_f, text="Xóa (Delete)", bg="#dc3545", fg="white", command=self.delete_user).pack(side="left", padx=5)

        self.notebook = ttk.Notebook(self.frame_crud)
        self.notebook.pack(fill="both", expand=True)
        self.tab_sv = Frame(self.notebook); self.tab_gv = Frame(self.notebook); self.tab_ad = Frame(self.notebook); self.tab_hp = Frame(self.notebook)
        self.notebook.add(self.tab_sv, text="👨‍🎓 Danh sách SV"); self.notebook.add(self.tab_gv, text="👨‍🏫 Danh sách GV"); self.notebook.add(self.tab_ad, text="📋 Danh sách Giáo vụ"); self.notebook.add(self.tab_hp, text="📚 Quản lý Học phần")

        # Treeviews - LƯU Ý: THÊM CỘT 'gpa' CHO SINH VIÊN
        self.tree_sv = ttk.Treeview(self.tab_sv, columns=('uid', 'name', 'email', 'gpa'), show='headings')
        self.tree_sv.heading('uid', text='MSSV'); self.tree_sv.heading('name', text='Họ Tên'); self.tree_sv.heading('email', text='Email'); self.tree_sv.heading('gpa', text='GPA')
        self.tree_sv.column('gpa', width=50, anchor='center')
        self.tree_sv.pack(fill="both", expand=True)
        self.tree_sv.bind("<ButtonRelease-1>", self.select_user)
        
        self.tree_gv = ttk.Treeview(self.tab_gv, columns=('uid', 'name', 'email'), show='headings')
        self.tree_gv.heading('uid', text='MSGV'); self.tree_gv.heading('name', text='Họ Tên'); self.tree_gv.heading('email', text='Email')
        self.tree_gv.pack(fill="both", expand=True)
        self.tree_gv.bind("<ButtonRelease-1>", self.select_user)
        
        self.tree_ad = ttk.Treeview(self.tab_ad, columns=('stt', 'uid', 'name', 'email'), show='headings')
        self.tree_ad.heading('stt', text='STT'); self.tree_ad.heading('uid', text='Mã NV'); self.tree_ad.heading('name', text='Họ Tên'); self.tree_ad.heading('email', text='Email')
        self.tree_ad.column('stt', width=50, anchor='center')
        self.tree_ad.pack(fill="both", expand=True)
        self.tree_ad.bind("<ButtonRelease-1>", self.select_user)
        
        hp_tool = Frame(self.tab_hp, bg="#f4f6f9")
        hp_tool.pack(fill="x", pady=5)
        Button(hp_tool, text="➕ Thêm HP mới", bg="#28a745", fg="white", font=("Segoe UI", 10, "bold"), command=self.open_add_course_popup).pack(side="left", padx=5)
        Button(hp_tool, text="➕ Mở Lớp mới", bg="#17a2b8", fg="white", font=("Segoe UI", 10, "bold"), command=self.open_add_class_popup).pack(side="left", padx=5)
        Button(hp_tool, text="❌ Xóa HP", bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold"), command=self.delete_course_ui).pack(side="left", padx=5)
        Button(hp_tool, text="➖ Xóa Lớp", bg="#ffc107", font=("Segoe UI", 10, "bold"), command=self.delete_class_ui).pack(side="left", padx=5)
        
        self.tree_hp = ttk.Treeview(self.tab_hp, columns=('stt', 'cid', 'name', 'creds', 'classes'), show='headings')
        self.tree_hp.heading('stt', text='STT'); self.tree_hp.heading('cid', text='Mã Học phần'); self.tree_hp.heading('name', text='Tên môn học'); self.tree_hp.heading('creds', text='Tín chỉ'); self.tree_hp.heading('classes', text='Các Lớp đang mở')
        self.tree_hp.column('stt', width=50, anchor='center'); self.tree_hp.column('creds', width=80, anchor='center')
        self.tree_hp.pack(fill="both", expand=True)

        # ==========================================
        # 2. GIAO DIỆN: XÉT HỌC BỔNG
        # ==========================================
        Label(self.frame_scholarship, text="Xét Duyệt Học Bổng", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        frame_input = Frame(self.frame_scholarship, bg="#f4f6f9"); frame_input.pack(anchor="w", pady=10)
        Label(frame_input, text="Số lượng suất:", font=("Segoe UI", 12), bg="#f4f6f9").pack(side="left")
        self.entry_slots = Entry(frame_input, font=("Segoe UI", 12), width=10); self.entry_slots.pack(side="left", padx=10)
        Button(frame_input, text="Chạy Engine", bg="#007bff", fg="white", command=self.run_scholarship).pack(side="left")
        self.tree_hb = ttk.Treeview(self.frame_scholarship, columns=('uid', 'name', 'score'), show='headings', height=10)
        self.tree_hb.heading('uid', text='Mã SV'); self.tree_hb.heading('name', text='Họ và Tên'); self.tree_hb.heading('score', text='Điểm Xét Tuyển')
        self.tree_hb.pack(fill="both", expand=True, pady=10)

        # ==========================================
        # 3. GIAO DIỆN: THỐNG KÊ GPA
        # ==========================================
        Label(self.frame_statistics, text="Thống kê GPA Toàn Khoa", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        Button(self.frame_statistics, text="Tải biểu đồ", font=("Segoe UI", 10), command=self.load_data).pack(anchor="w", pady=5)
        self.content_frame = Frame(self.frame_statistics, bg="#f4f6f9"); self.content_frame.pack(fill="both", expand=True, pady=10)
        self.tree_stat = ttk.Treeview(self.content_frame, columns=('loai', 'so_luong'), show='headings', height=6)
        self.tree_stat.heading('loai', text='Xếp loại'); self.tree_stat.heading('so_luong', text='Số sinh viên')
        self.tree_stat.pack(side="left", anchor="n", padx=(0, 20))
        self.chart_frame = Frame(self.content_frame, bg="#f4f6f9"); self.chart_frame.pack(side="left", fill="both", expand=True)

        # ==========================================
        # 4. GIAO DIỆN: QUẢN LÝ HỌC VỤ
        # ==========================================
        Label(self.frame_management, text="Quản lý Cảnh cáo & Báo cáo", font=("Segoe UI", 18, "bold"), bg="#f4f6f9").pack(anchor="w", pady=10)
        tool_frame = Frame(self.frame_management, bg="#f4f6f9"); tool_frame.pack(fill="x", pady=5)
        Button(tool_frame, text="🔄 Tải DS Nguy hiểm", command=self.load_at_risk_students).pack(side="left", padx=5)
        Button(tool_frame, text="⚠️ Cảnh Cáo", bg="orange", command=lambda: self.change_status("Cảnh cáo học vụ")).pack(side="left", padx=5)
        Button(tool_frame, text="⛔ Đình Chỉ", bg="red", fg="white", command=lambda: self.change_status("Đình chỉ học")).pack(side="left", padx=5)
        Button(tool_frame, text="⬇️ Xuất Excel", bg="#28a745", fg="white", command=self.export_excel).pack(side="right", padx=5)
        self.tree_mng = ttk.Treeview(self.frame_management, columns=('uid', 'name', 'gpa', 'att', 'status'), show='headings', height=15)
        self.tree_mng.heading('uid', text='Mã SV'); self.tree_mng.heading('name', text='Họ và Tên'); self.tree_mng.heading('gpa', text='GPA'); self.tree_mng.heading('att', text='Chuyên cần'); self.tree_mng.heading('status', text='Trạng thái')
        self.tree_mng.pack(fill="both", expand=True, pady=10)

        self.show_crud()
        self.window.mainloop()

    # ==========================================
    # CÁC HÀM ĐIỀU HƯỚNG VÀ LOAD DATA
    # ==========================================
    def hide_all(self):
        self.frame_crud.pack_forget(); self.frame_scholarship.pack_forget(); self.frame_statistics.pack_forget(); self.frame_management.pack_forget()

    def show_crud(self): self.hide_all(); self.frame_crud.pack(fill="both", expand=True); self.load_users()
    def show_scholarship(self): self.hide_all(); self.frame_scholarship.pack(fill="both", expand=True)
    def show_statistics(self): self.hide_all(); self.frame_statistics.pack(fill="both", expand=True)
    def show_management(self): self.hide_all(); self.frame_management.pack(fill="both", expand=True)

    def load_users(self):
        for tree in [self.tree_sv, self.tree_gv, self.tree_ad, self.tree_hp]: [tree.delete(row) for row in tree.get_children()]
            
        users = self.staff_ctr.get_all_users()
        c_ad = 1
        for u in users:
            if u['role'] == 'Student': 
                # Chèn thêm GPA vào bảng Sinh viên
                self.tree_sv.insert('', 'end', values=(u['uid'], u['name'], u['email'], u.get('gpa', 0.0)))
            elif u['role'] == 'Lecturer': self.tree_gv.insert('', 'end', values=(u['uid'], u['name'], u['email']))
            elif u['role'] == 'Staff': self.tree_ad.insert('', 'end', values=(c_ad, u['uid'], u['name'], u['email'])); c_ad += 1
            
        for idx, c in enumerate(self.staff_ctr.get_all_courses(), 1): 
            self.tree_hp.insert('', 'end', values=(idx, c['id'], c['name'], c['credits'], c['classes']))

    def select_user(self, event):
        tab = self.notebook.index(self.notebook.select())
        if tab == 3: return
        tree = [self.tree_sv, self.tree_gv, self.tree_ad][tab]
        sel = tree.selection()
        if sel:
            item = tree.item(sel[0])['values']
            self.entry_uid.config(state="normal"); self.entry_uid.delete(0, END); self.entry_name.delete(0, END); self.entry_email.delete(0, END); self.entry_pwd.delete(0, END)
            
            if tab == 2: 
                self.entry_uid.insert(0, item[1]); self.entry_name.insert(0, item[2]); self.entry_email.insert(0, item[3])
            else: 
                self.entry_uid.insert(0, item[0]); self.entry_name.insert(0, item[1]); self.entry_email.insert(0, item[2])
            
            self.cmb_role.set(["Student", "Lecturer", "Staff"][tab])
            self.entry_pwd.insert(0, "******")
            self.entry_uid.config(state="disabled")

    def add_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        if not all([uid, name, email, pwd, role]): messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin và chọn Vai trò!"); return
        success, msg = self.staff_ctr.create_user(uid, name, email, pwd, role)
        if success: messagebox.showinfo("OK", msg); self.load_users(); self.clear_form()
        else: messagebox.showerror("Lỗi", msg)

    def update_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        if not all([uid, name, email, pwd, role]): messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin và chọn Vai trò!"); return
        success, msg = self.staff_ctr.update_user(uid, name, email, pwd, role)
        if success: messagebox.showinfo("OK", msg); self.load_users()
        else: messagebox.showerror("Lỗi", msg)

    def delete_user(self):
        success, msg = self.staff_ctr.delete_user(self.entry_uid.get())
        if success: messagebox.showinfo("OK", msg); self.load_users(); self.clear_form()
        else: messagebox.showerror("Lỗi", msg)

    def clear_form(self):
        self.entry_uid.config(state="normal"); self.entry_uid.delete(0, END); self.entry_name.delete(0, END); self.entry_email.delete(0, END); self.entry_pwd.delete(0, END)
        self.cmb_role.set("Student")

    # ==========================================
    # CÁC POPUP & CHỨC NĂNG HỌC PHẦN
    # ==========================================
    def open_add_course_popup(self):
        p = Toplevel(self.window); p.title("Thêm Học Phần"); p.geometry("400x350"); p.configure(bg="white"); p.grab_set()
        Label(p, text="TẠO MÔN HỌC MỚI", font=("Segoe UI", 14, "bold"), bg="white", fg="#28a745").pack(pady=15)
        Label(p, text="Mã Học phần:", bg="white").pack(anchor="w", padx=30); e_cid = Entry(p, font=("Segoe UI", 11)); e_cid.pack(fill="x", padx=30, pady=(0, 10))
        Label(p, text="Tên môn học:", bg="white").pack(anchor="w", padx=30); e_name = Entry(p, font=("Segoe UI", 11)); e_name.pack(fill="x", padx=30, pady=(0, 10))
        Label(p, text="Số tín chỉ:", bg="white").pack(anchor="w", padx=30); e_creds = Entry(p, font=("Segoe UI", 11)); e_creds.pack(fill="x", padx=30, pady=(0, 10))
        
        def submit():
            try:
                success, msg = self.staff_ctr.create_course(e_cid.get(), e_name.get(), int(e_creds.get()))
                if success: messagebox.showinfo("OK", msg, parent=p); self.load_users(); p.destroy()
                else: messagebox.showerror("Lỗi", msg, parent=p)
            except ValueError: messagebox.showerror("Lỗi", "Tín chỉ phải là số nguyên!", parent=p)
        Button(p, text="💾 Lưu Môn học", bg="#28a745", fg="white", font=("Segoe UI", 11, "bold"), command=submit).pack(pady=15)

    def open_add_class_popup(self):
        p = Toplevel(self.window); p.title("Mở Lớp Học Phần"); p.geometry("450x380"); p.configure(bg="white"); p.grab_set()
        Label(p, text="MỞ LỚP HỌC PHẦN", font=("Segoe UI", 14, "bold"), bg="white", fg="#17a2b8").pack(pady=15)
        Label(p, text="Mã Lớp:", bg="white").pack(anchor="w", padx=30); e_cls = Entry(p, font=("Segoe UI", 11)); e_cls.pack(fill="x", padx=30, pady=(0, 10))
        Label(p, text="Mã Học phần:", bg="white").pack(anchor="w", padx=30); e_cid = Entry(p, font=("Segoe UI", 11)); e_cid.pack(fill="x", padx=30, pady=(0, 10))
        Label(p, text="MSGV phụ trách:", bg="white").pack(anchor="w", padx=30); e_lec = Entry(p, font=("Segoe UI", 11)); e_lec.pack(fill="x", padx=30, pady=(0, 10))
        Label(p, text="Sĩ số tối đa:", bg="white").pack(anchor="w", padx=30); e_cap = Entry(p, font=("Segoe UI", 11)); e_cap.insert(0, "40"); e_cap.pack(fill="x", padx=30, pady=(0, 10))
        
        def submit():
            cls, cid, lec, cap_str = e_cls.get().strip(), e_cid.get().strip(), e_lec.get().strip(), e_cap.get().strip()
            if not all([cls, cid, lec, cap_str]): messagebox.showwarning("Lỗi", "Nhập đủ thông tin!", parent=p); return
            try: cap = int(cap_str)
            except: messagebox.showwarning("Lỗi", "Sĩ số là số nguyên!", parent=p); return
            success, msg = self.staff_ctr.create_course_class(cls, cid, lec, cap)
            if success: messagebox.showinfo("OK", msg, parent=p); self.load_users(); p.destroy()
            else: messagebox.showerror("Lỗi", msg, parent=p)
        Button(p, text="💾 Mở Lớp mới", bg="#17a2b8", fg="white", font=("Segoe UI", 11, "bold"), command=submit).pack(pady=15)

    def delete_course_ui(self):
        sel = self.tree_hp.selection()
        if not sel: messagebox.showwarning("Chưa chọn", "Chọn 1 môn học để xóa!"); return
        cid = self.tree_hp.item(sel[0])['values'][1]
        if messagebox.askyesno("Cảnh báo", f"Xóa vĩnh viễn môn '{cid}'?"): 
            success, msg = self.staff_ctr.delete_course(cid)
            if success: messagebox.showinfo("OK", msg); self.load_users()
            else: messagebox.showerror("Lỗi", msg)

    def delete_class_ui(self):
        cid = simpledialog.askstring("Xóa lớp", "Nhập Mã Lớp cần xóa:")
        if cid: 
            if messagebox.askyesno("Xác nhận", f"Xóa lớp '{cid}'?"):
                success, msg = self.staff_ctr.delete_course_class(cid.strip())
                if success: messagebox.showinfo("OK", msg); self.load_users()
                else: messagebox.showerror("Lỗi", msg)

    # ==========================================
    # LOGIC: HỌC BỔNG, THỐNG KÊ, CẢNH CÁO
    # ==========================================
    def load_at_risk_students(self):
        for row in self.tree_mng.get_children(): self.tree_mng.delete(row)
        students = self.staff_ctr.get_at_risk_students()
        for s in students: self.tree_mng.insert('', 'end', values=(s['uid'], s['name'], s['gpa'], s['att'], s['status']))
    
    def change_status(self, new_status):
        selected = self.tree_mng.selection()
        if not selected: messagebox.showwarning("Chưa chọn", "Click chọn 1 SV!"); return
        item = self.tree_mng.item(selected[0])
        success, msg = self.staff_ctr.update_student_status(str(item['values'][0]), new_status)
        if success: messagebox.showinfo("OK", msg); self.load_at_risk_students()
        else: messagebox.showerror("Lỗi", msg)

    def export_excel(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")], title="Lưu")
        if file_path:
            success, msg = self.staff_ctr.export_report_to_excel(file_path)
            if success: messagebox.showinfo("OK", msg)
            else: messagebox.showerror("Lỗi", msg)

    def run_scholarship(self):
        for row in self.tree_hb.get_children(): self.tree_hb.delete(row)
        try:
            winners = self.staff_ctr.execute_scholarship_filter(int(self.entry_slots.get()))
            for w in winners: self.tree_hb.insert('', 'end', values=(w['uid'], w['name'], f"{w['score']:.2f}"))
        except ValueError: messagebox.showerror("Lỗi", "Nhập số nguyên!")

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