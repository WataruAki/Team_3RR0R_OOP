import customtkinter as ctk
from tkinter import ttk, messagebox, filedialog, simpledialog, END
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from controllers.controllers import AcademicStaffController, MainController

ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

# Màu chuẩn HyperOS
APP_BG = ("#F3F4F6", "#000000")
CARD_BG = ("#FFFFFF", "#1C1C1E")

class ASWindow:
    def __init__(self, main_controller):
        self.staff_ctr = AcademicStaffController(main_controller)
        self.window = ctk.CTk()
        self.window.geometry("1150x750")
        self.window.title("BCSE - Giáo Vụ")
        self.window.configure(fg_color=APP_BG)

        # ==========================================
        # SIDEBAR (Thanh điều hướng)
        # ==========================================
        self.sidebar = ctk.CTkFrame(self.window, width=240, corner_radius=0, fg_color=CARD_BG)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="BCSE Admin", font=("Segoe UI", 24, "bold"), text_color="#3B82F6").pack(pady=(35, 30))
        
        btn_opts = {"fg_color": "transparent", "text_color": ("gray20", "gray80"), "hover_color": ("#E5E7EB", "#2C2C2E"), 
                    "font": ("Segoe UI", 14, "bold"), "anchor": "w", "height": 45, "corner_radius": 12}
        
        ctk.CTkButton(self.sidebar, text="🏢  Quản lý Hệ thống", command=self.show_crud, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="🎓  Xét Học Bổng", command=self.show_scholarship, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="📊  Thống kê GPA", command=self.show_statistics, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="⚠️  Quản lý Học vụ", command=self.show_management, **btn_opts).pack(fill="x", padx=15, pady=5)

        # NÚT THEME
        self.btn_theme = ctk.CTkButton(self.sidebar, text="☀️ Light Mode" if ctk.get_appearance_mode()=="Dark" else "🌙 Dark Mode", 
                                       command=self.toggle_theme, fg_color=("gray85", "#2C2C2E"), text_color=("black", "white"), font=("Segoe UI", 12, "bold"), corner_radius=20)
        self.btn_theme.pack(side="bottom", fill="x", padx=20, pady=(0, 25))

        # PROFILE BADGE
        user = main_controller.current_user
        u_name = getattr(user, 'name', 'Trần Thị Giáo Vụ')
        u_id = getattr(user, 'user_id', '001')
        initials = "".join([w[0] for w in u_name.split()[-2:]]).upper() if len(u_name.split()) >= 2 else u_name[:2].upper()

        self.profile_card = ctk.CTkFrame(self.sidebar, corner_radius=15, fg_color=("gray85", "#2C2C2E"))
        self.profile_card.pack(side="bottom", fill="x", padx=15, pady=(0, 20))

        self.avatar = ctk.CTkLabel(self.profile_card, text=initials, font=("Segoe UI", 16, "bold"), 
                                   width=46, height=46, corner_radius=23, fg_color="#3B82F6", text_color="white")
        self.avatar.pack(side="left", padx=10, pady=10)

        info_f = ctk.CTkFrame(self.profile_card, fg_color="transparent")
        info_f.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(info_f, text=u_name, font=("Segoe UI", 13, "bold"), text_color=("black", "white"), anchor="w").pack(fill="x")
        ctk.CTkLabel(info_f, text=f"UID: {u_id}", font=("Consolas", 11), text_color=("gray40", "gray60"), anchor="w").pack(fill="x")

        # ==========================================
        # KHU VỰC MAIN CONTAINER 
        # ==========================================
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)

        self.frame_crud = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_scholarship = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_statistics = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_management = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        
        # Cấu hình UI xịn xò
        action_btn = {"font": ("Segoe UI", 13, "bold"), "height": 40, "corner_radius": 20, "cursor": "hand2"}
        entry_opts = {"height": 40, "font": ("Segoe UI", 13), "border_width": 0, "corner_radius": 8, "fg_color": ("#F3F4F6", "#2C2C2E")}
        label_opts = {"text_color": ("gray20", "gray80"), "font": ("Segoe UI", 12, "bold")}

        # 1. GIAO DIỆN CRUD
        ctk.CTkLabel(self.frame_crud, text="Quản lý Tài khoản & Học phần", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        form_frame = ctk.CTkFrame(self.frame_crud, fg_color=CARD_BG, corner_radius=15)
        form_frame.pack(fill="x", pady=(0, 20), ipadx=15, ipady=15)
        
        ctk.CTkLabel(form_frame, text="Mã ID:", **label_opts).grid(row=0, column=0, padx=(15, 10), pady=12, sticky="w"); self.entry_uid = ctk.CTkEntry(form_frame, width=180, **entry_opts); self.entry_uid.grid(row=0, column=1, padx=(0, 30))
        ctk.CTkLabel(form_frame, text="Họ Tên:", **label_opts).grid(row=0, column=2, padx=(0, 10), pady=12, sticky="w"); self.entry_name = ctk.CTkEntry(form_frame, width=300, **entry_opts); self.entry_name.grid(row=0, column=3, padx=(0, 15))
        ctk.CTkLabel(form_frame, text="Email:", **label_opts).grid(row=1, column=0, padx=(15, 10), pady=12, sticky="w"); self.entry_email = ctk.CTkEntry(form_frame, width=180, **entry_opts); self.entry_email.grid(row=1, column=1, padx=(0, 30))
        ctk.CTkLabel(form_frame, text="Mật khẩu:", **label_opts).grid(row=1, column=2, padx=(0, 10), pady=12, sticky="w"); self.entry_pwd = ctk.CTkEntry(form_frame, width=300, show="*", **entry_opts); self.entry_pwd.grid(row=1, column=3, padx=(0, 15))
        ctk.CTkLabel(form_frame, text="Vai trò:", **label_opts).grid(row=2, column=0, padx=(15, 10), pady=12, sticky="w"); self.cmb_role = ctk.CTkComboBox(form_frame, values=["Student", "Lecturer", "Staff"], width=180, **entry_opts); self.cmb_role.set("Student"); self.cmb_role.grid(row=2, column=1, padx=(0, 30))
        
        btn_f = ctk.CTkFrame(form_frame, fg_color="transparent"); btn_f.grid(row=3, column=0, columnspan=4, pady=(20, 5))
        ctk.CTkButton(btn_f, text="Làm mới", fg_color="#6B7280", hover_color="#4B5563", command=self.clear_form, **action_btn).pack(side="left", padx=8)
        ctk.CTkButton(btn_f, text="Thêm Mới", fg_color="#10B981", hover_color="#059669", command=self.add_user, **action_btn).pack(side="left", padx=8)
        ctk.CTkButton(btn_f, text="Cập nhật", fg_color="#3B82F6", hover_color="#2563EB", command=self.update_user, **action_btn).pack(side="left", padx=8)
        ctk.CTkButton(btn_f, text="Xóa", fg_color="#EF4444", hover_color="#DC2626", command=self.delete_user, **action_btn).pack(side="left", padx=8)

        self.tabview = ctk.CTkTabview(self.frame_crud, fg_color=CARD_BG, corner_radius=15, segmented_button_selected_color="#3B82F6")
        self.tabview.pack(fill="both", expand=True)
        self.tab_sv = self.tabview.add("👨‍🎓 Sinh viên"); self.tab_gv = self.tabview.add("👨‍🏫 Giảng viên"); self.tab_ad = self.tabview.add("📋 Giáo vụ"); self.tab_hp = self.tabview.add("📚 Học phần")

        self.tree_sv = ttk.Treeview(self.tab_sv, columns=('uid', 'name', 'email', 'gpa'), show='headings'); self.tree_sv.heading('uid', text='MSSV'); self.tree_sv.heading('name', text='Họ và Tên'); self.tree_sv.heading('email', text='Email'); self.tree_sv.heading('gpa', text='GPA'); self.tree_sv.column('gpa', width=60, anchor='center'); self.tree_sv.pack(fill="both", expand=True, pady=(10, 0))
        self.tree_gv = ttk.Treeview(self.tab_gv, columns=('uid', 'name', 'email'), show='headings'); self.tree_gv.heading('uid', text='MSGV'); self.tree_gv.heading('name', text='Họ và Tên'); self.tree_gv.heading('email', text='Email'); self.tree_gv.pack(fill="both", expand=True, pady=(10, 0))
        self.tree_ad = ttk.Treeview(self.tab_ad, columns=('stt', 'uid', 'name', 'email'), show='headings'); self.tree_ad.heading('stt', text='STT'); self.tree_ad.heading('uid', text='Mã NV'); self.tree_ad.heading('name', text='Họ và Tên'); self.tree_ad.heading('email', text='Email'); self.tree_ad.column('stt', width=50, anchor='center'); self.tree_ad.pack(fill="both", expand=True, pady=(10, 0))
        
        hp_tool = ctk.CTkFrame(self.tab_hp, fg_color="transparent"); hp_tool.pack(fill="x", pady=10)
        ctk.CTkButton(hp_tool, text="➕ Môn Mới", fg_color="#10B981", hover_color="#059669", command=self.open_add_course_popup, **action_btn).pack(side="left", padx=5)
        ctk.CTkButton(hp_tool, text="➕ Lớp Học", fg_color="#06B6D4", hover_color="#0891B2", command=self.open_add_class_popup, **action_btn).pack(side="left", padx=5)
        ctk.CTkButton(hp_tool, text="❌ Xóa Môn", fg_color="#EF4444", hover_color="#DC2626", command=self.delete_course_ui, **action_btn).pack(side="left", padx=5)
        ctk.CTkButton(hp_tool, text="➖ Xóa Lớp", fg_color="#F59E0B", hover_color="#D97706", command=self.delete_class_ui, **action_btn).pack(side="left", padx=5)
        self.tree_hp = ttk.Treeview(self.tab_hp, columns=('stt', 'cid', 'name', 'creds', 'classes'), show='headings'); self.tree_hp.heading('stt', text='STT'); self.tree_hp.heading('cid', text='Mã Học phần'); self.tree_hp.heading('name', text='Tên môn học'); self.tree_hp.heading('creds', text='Tín chỉ'); self.tree_hp.heading('classes', text='Các Lớp đang mở'); self.tree_hp.column('stt', width=50, anchor='center'); self.tree_hp.column('creds', width=80, anchor='center'); self.tree_hp.pack(fill="both", expand=True, pady=(10, 0))
        for t in [self.tree_sv, self.tree_gv, self.tree_ad, self.tree_hp]: t.bind("<ButtonRelease-1>", self.select_user)

        # 2. XÉT HỌC BỔNG
        ctk.CTkLabel(self.frame_scholarship, text="Xét Duyệt Học Bổng", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        f_in = ctk.CTkFrame(self.frame_scholarship, fg_color=CARD_BG, corner_radius=15); f_in.pack(fill="x", pady=(0, 20), ipadx=15, ipady=15)
        ctk.CTkLabel(f_in, text="Số lượng suất:", font=("Segoe UI", 14, "bold"), text_color=("gray20", "gray80")).pack(side="left", padx=15)
        self.entry_slots = ctk.CTkEntry(f_in, width=120, **entry_opts); self.entry_slots.pack(side="left", padx=10)
        ctk.CTkButton(f_in, text="Khởi Duyệt", fg_color="#3B82F6", hover_color="#2563EB", command=self.run_scholarship, **action_btn).pack(side="left", padx=15)
        self.tree_hb = ttk.Treeview(self.frame_scholarship, columns=('uid', 'name', 'score'), show='headings'); self.tree_hb.heading('uid', text='Mã SV'); self.tree_hb.heading('name', text='Họ và Tên'); self.tree_hb.heading('score', text='Điểm Xét Tuyển'); self.tree_hb.pack(fill="both", expand=True)

        # 3. THỐNG KÊ GPA (CHART CÓ BÓNG ĐỔ)
        ctk.CTkLabel(self.frame_statistics, text="Thống kê GPA Toàn Khoa", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        ctk.CTkButton(self.frame_statistics, text="Tải & Vẽ Biểu Đồ", fg_color="#8B5CF6", hover_color="#7C3AED", command=self.load_data, **action_btn).pack(anchor="w", pady=(0, 20))
        self.content_frame = ctk.CTkFrame(self.frame_statistics, fg_color="transparent"); self.content_frame.pack(fill="both", expand=True)
        self.tree_stat = ttk.Treeview(self.content_frame, columns=('loai', 'so_luong'), show='headings'); self.tree_stat.heading('loai', text='Xếp loại'); self.tree_stat.heading('so_luong', text='Số sinh viên'); self.tree_stat.pack(side="left", fill="y", padx=(0, 25))
        self.chart_frame = ctk.CTkFrame(self.content_frame, fg_color=CARD_BG, corner_radius=15); self.chart_frame.pack(side="left", fill="both", expand=True)

        # 4. QUẢN LÝ HỌC VỤ
        ctk.CTkLabel(self.frame_management, text="Quản lý Cảnh cáo Học vụ", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        t_f = ctk.CTkFrame(self.frame_management, fg_color="transparent"); t_f.pack(fill="x", pady=(0, 20))
        ctk.CTkButton(t_f, text="Quét DS Nguy hiểm", fg_color="#6B7280", command=self.load_at_risk_students, **action_btn).pack(side="left", padx=(0, 10))
        ctk.CTkButton(t_f, text="Cảnh Cáo", fg_color="#F59E0B", command=lambda: self.change_status("Cảnh cáo học vụ"), **action_btn).pack(side="left", padx=8)
        ctk.CTkButton(t_f, text="Đình Chỉ", fg_color="#EF4444", command=lambda: self.change_status("Đình chỉ học"), **action_btn).pack(side="left", padx=8)
        ctk.CTkButton(t_f, text="Xuất File Excel", fg_color="#10B981", command=self.export_excel, **action_btn).pack(side="right")
        self.tree_mng = ttk.Treeview(self.frame_management, columns=('uid', 'name', 'gpa', 'att', 'status'), show='headings'); self.tree_mng.heading('uid', text='Mã SV'); self.tree_mng.heading('name', text='Họ và Tên'); self.tree_mng.heading('gpa', text='GPA'); self.tree_mng.heading('att', text='Chuyên cần'); self.tree_mng.heading('status', text='Trạng thái'); self.tree_mng.pack(fill="both", expand=True)

        self.apply_treeview_style(ctk.get_appearance_mode())
        self.show_crud()
        self.window.mainloop()

    def toggle_theme(self):
        new_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.apply_treeview_style(new_mode)
        self.btn_theme.configure(text="🌙 Dark Mode" if new_mode=="Light" else "☀️ Light Mode")
        if len(self.chart_frame.winfo_children()) > 0: self.load_data()

    def apply_treeview_style(self, mode):
        style = ttk.Style()
        style.theme_use("clam")
        if mode == "Dark":
            style.configure("Treeview", background="#1C1C1E", foreground="white", fieldbackground="#1C1C1E", rowheight=40, borderwidth=0, font=("Segoe UI", 12))
            style.map('Treeview', background=[('selected', '#3B82F6')])
            style.configure("Treeview.Heading", background="#2C2C2E", foreground="white", font=("Segoe UI", 12, "bold"), borderwidth=0, padding=12)
        else:
            style.configure("Treeview", background="#FFFFFF", foreground="#1F2937", fieldbackground="#FFFFFF", rowheight=40, borderwidth=0, font=("Segoe UI", 12))
            style.map('Treeview', background=[('selected', '#DBEAFE')])
            style.configure("Treeview.Heading", background="#F9FAFB", foreground="#6B7280", font=("Segoe UI", 12, "bold"), borderwidth=0, padding=12)

    # --- ĐIỀU HƯỚNG VÀ LOAD DATA ---
    def hide_all(self): self.frame_crud.pack_forget(); self.frame_scholarship.pack_forget(); self.frame_statistics.pack_forget(); self.frame_management.pack_forget()
    def show_crud(self): self.hide_all(); self.frame_crud.pack(fill="both", expand=True); self.load_users()
    def show_scholarship(self): self.hide_all(); self.frame_scholarship.pack(fill="both", expand=True)
    def show_statistics(self): self.hide_all(); self.frame_statistics.pack(fill="both", expand=True)
    def show_management(self): self.hide_all(); self.frame_management.pack(fill="both", expand=True)

    def load_users(self):
        for tree in [self.tree_sv, self.tree_gv, self.tree_ad, self.tree_hp]: [tree.delete(row) for row in tree.get_children()]
        users = self.staff_ctr.get_all_users()
        c_ad = 1
        for u in users:
            if u['role'] == 'Student': self.tree_sv.insert('', 'end', values=(u['uid'], u['name'], u['email'], u.get('gpa', 0.0)))
            elif u['role'] == 'Lecturer': self.tree_gv.insert('', 'end', values=(u['uid'], u['name'], u['email']))
            elif u['role'] == 'Staff': self.tree_ad.insert('', 'end', values=(c_ad, u['uid'], u['name'], u['email'])); c_ad += 1
        for idx, c in enumerate(self.staff_ctr.get_all_courses(), 1): self.tree_hp.insert('', 'end', values=(idx, c['id'], c['name'], c['credits'], c['classes']))

    def select_user(self, event):
        tab_name = self.tabview.get()
        if tab_name == "📚 Học phần": return
        tree, idx = {"👨‍🎓 Sinh viên": (self.tree_sv, 0), "👨‍🏫 Giảng viên": (self.tree_gv, 1), "📋 Giáo vụ": (self.tree_ad, 2)}[tab_name]
        sel = tree.selection()
        if sel:
            item = tree.item(sel[0])['values']
            self.entry_uid.configure(state="normal"); self.entry_uid.delete(0, END); self.entry_name.delete(0, END); self.entry_email.delete(0, END); self.entry_pwd.delete(0, END)
            if idx == 2: self.entry_uid.insert(0, item[1]); self.entry_name.insert(0, item[2]); self.entry_email.insert(0, item[3])
            else: self.entry_uid.insert(0, item[0]); self.entry_name.insert(0, item[1]); self.entry_email.insert(0, item[2])
            self.cmb_role.set(["Student", "Lecturer", "Staff"][idx]); self.entry_pwd.insert(0, "******"); self.entry_uid.configure(state="disabled")

    def add_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        if not all([uid, name, email, pwd, role]): messagebox.showwarning("Lỗi", "Vui lòng nhập đủ thông tin!"); return
        success, msg = self.staff_ctr.create_user(uid, name, email, pwd, role)
        if success: messagebox.showinfo("OK", msg); self.load_users(); self.clear_form()
        else: messagebox.showerror("Lỗi", msg)

    def update_user(self):
        uid, name, email, pwd, role = self.entry_uid.get(), self.entry_name.get(), self.entry_email.get(), self.entry_pwd.get(), self.cmb_role.get()
        success, msg = self.staff_ctr.update_user(uid, name, email, pwd, role)
        if success: messagebox.showinfo("OK", msg); self.load_users()
        else: messagebox.showerror("Lỗi", msg)

    def delete_user(self):
        success, msg = self.staff_ctr.delete_user(self.entry_uid.get())
        if success: messagebox.showinfo("OK", msg); self.load_users(); self.clear_form()
        else: messagebox.showerror("Lỗi", msg)

    def clear_form(self):
        self.entry_uid.configure(state="normal"); self.entry_uid.delete(0, END); self.entry_name.delete(0, END); self.entry_email.delete(0, END); self.entry_pwd.delete(0, END); self.cmb_role.set("Student")

    def open_add_course_popup(self):
        p = ctk.CTkToplevel(self.window); p.title("Thêm Học Phần"); p.geometry("450x450"); p.attributes("-topmost", True); p.configure(fg_color=APP_BG)
        ctk.CTkLabel(p, text="MÔN HỌC MỚI", font=("Segoe UI", 20, "bold"), text_color="#10B981").pack(pady=25)
        opts = {"width": 320, "height": 45, "font": ("Segoe UI", 13), "corner_radius": 8, "border_width": 0, "fg_color": CARD_BG}
        e_cid = ctk.CTkEntry(p, placeholder_text="Mã Học phần (VD: CSE101)", **opts); e_cid.pack(pady=10)
        e_name = ctk.CTkEntry(p, placeholder_text="Tên môn học", **opts); e_name.pack(pady=10)
        e_creds = ctk.CTkEntry(p, placeholder_text="Số tín chỉ", **opts); e_creds.pack(pady=10)
        def submit():
            try:
                success, msg = self.staff_ctr.create_course(e_cid.get(), e_name.get(), int(e_creds.get()))
                if success: self.load_users(); p.destroy()
                else: messagebox.showerror("Lỗi", msg, parent=p)
            except ValueError: messagebox.showerror("Lỗi", "Tín chỉ phải là số nguyên!", parent=p)
        ctk.CTkButton(p, text="Lưu Môn học", fg_color="#10B981", hover_color="#059669", font=("Segoe UI", 14, "bold"), corner_radius=20, height=45, command=submit).pack(pady=25)

    def open_add_class_popup(self):
        p = ctk.CTkToplevel(self.window); p.title("Mở Lớp Học Phần"); p.geometry("450x500"); p.attributes("-topmost", True); p.configure(fg_color=APP_BG)
        ctk.CTkLabel(p, text="MỞ LỚP HỌC", font=("Segoe UI", 20, "bold"), text_color="#06B6D4").pack(pady=25)
        opts = {"width": 320, "height": 45, "font": ("Segoe UI", 13), "corner_radius": 8, "border_width": 0, "fg_color": CARD_BG}
        e_cls = ctk.CTkEntry(p, placeholder_text="Mã Lớp (VD: CSE3011_C3)", **opts); e_cls.pack(pady=10)
        e_cid = ctk.CTkEntry(p, placeholder_text="Mã Học phần (VD: CSE3011)", **opts); e_cid.pack(pady=10)
        e_lec = ctk.CTkEntry(p, placeholder_text="MSGV phụ trách (VD: VJU001)", **opts); e_lec.pack(pady=10)
        e_cap = ctk.CTkEntry(p, placeholder_text="Sĩ số tối đa", **opts); e_cap.insert(0, "40"); e_cap.pack(pady=10)
        def submit():
            cls, cid, lec, cap_str = e_cls.get().strip(), e_cid.get().strip(), e_lec.get().strip(), e_cap.get().strip()
            if not all([cls, cid, lec, cap_str]): return
            try: cap = int(cap_str)
            except: messagebox.showwarning("Lỗi", "Sĩ số là số nguyên!", parent=p); return
            success, msg = self.staff_ctr.create_course_class(cls, cid, lec, cap)
            if success: self.load_users(); p.destroy()
            else: messagebox.showerror("Lỗi", msg, parent=p)
        ctk.CTkButton(p, text="Mở Lớp mới", fg_color="#06B6D4", hover_color="#0891B2", font=("Segoe UI", 14, "bold"), corner_radius=20, height=45, command=submit).pack(pady=25)

    def delete_course_ui(self):
        sel = self.tree_hp.selection()
        if not sel: return
        cid = self.tree_hp.item(sel[0])['values'][1]
        if messagebox.askyesno("Cảnh báo", f"Xóa vĩnh viễn môn '{cid}'?"): 
            self.staff_ctr.delete_course(cid); self.load_users()

    def delete_class_ui(self):
        cid = simpledialog.askstring("Xóa lớp", "Nhập Mã Lớp cần xóa:")
        if cid and messagebox.askyesno("Xác nhận", f"Xóa lớp '{cid}'?"):
            self.staff_ctr.delete_course_class(cid.strip()); self.load_users()

    def load_at_risk_students(self):
        for row in self.tree_mng.get_children(): self.tree_mng.delete(row)
        for s in self.staff_ctr.get_at_risk_students(): self.tree_mng.insert('', 'end', values=(s['uid'], s['name'], s['gpa'], s['att'], s['status']))
    
    def change_status(self, new_status):
        sel = self.tree_mng.selection()
        if sel: self.staff_ctr.update_student_status(str(self.tree_mng.item(sel[0])['values'][0]), new_status); self.load_at_risk_students()

    def export_excel(self):
        fp = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if fp: self.staff_ctr.export_report_to_excel(fp)

    def run_scholarship(self):
        for row in self.tree_hb.get_children(): self.tree_hb.delete(row)
        try:
            for w in self.staff_ctr.execute_scholarship_filter(int(self.entry_slots.get())): self.tree_hb.insert('', 'end', values=(w['uid'], w['name'], f"{w['score']:.2f}"))
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
        
        is_dark = ctk.get_appearance_mode() == "Dark"
        fig.patch.set_facecolor('#1C1C1E' if is_dark else '#FFFFFF')
        
        ax = fig.add_subplot(111)
        if not sizes: 
            ax.text(0.5, 0.5, "Chưa có dữ liệu", ha='center', va='center', color="white" if is_dark else "black")
        else:
            explode = [0.06] * len(sizes) 
            ax.pie(sizes, explode=explode, labels=labels, colors=['#EF4444', '#3B82F6', '#10B981', '#F59E0B'], 
                   autopct='%1.1f%%', startangle=140, shadow=True, 
                   textprops={'color':"white" if is_dark else "black", 'fontweight': 'bold'})
            ax.set_title("Tỉ lệ Học lực Toàn khóa", pad=20, fontweight='bold', color="white" if is_dark else "#111827")
            
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame) 
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = type('obj', (object,), {'role': 'Staff', 'name': 'Trần Thị Giáo Vụ', 'user_id': '001'})() 
    ASWindow(fake_ctrl)