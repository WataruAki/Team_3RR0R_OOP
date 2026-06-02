import customtkinter as ctk
from tkinter import ttk, messagebox, END
from controllers.controllers import StudentController, MainController

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

APP_BG = ("#F3F4F6", "#000000")
CARD_BG = ("#FFFFFF", "#1C1C1E")

class StudentWindow:
    def __init__(self, main_controller):
        self.student_ctr = StudentController(main_controller)
        self.window = ctk.CTk()
        self.window.geometry("1150x750")
        self.window.title("BCSE - Sinh Viên")
        self.window.configure(fg_color=APP_BG)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self.window, width=240, corner_radius=0, fg_color=CARD_BG)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="SINH VIÊN", font=("Segoe UI", 24, "bold"), text_color="#10B981").pack(pady=(35, 30))
        btn_opts = {"fg_color": "transparent", "text_color": ("gray20", "gray80"), "hover_color": ("#E5E7EB", "#2C2C2E"), 
                    "font": ("Segoe UI", 14, "bold"), "anchor": "w", "height": 45, "corner_radius": 12}
        
        ctk.CTkButton(self.sidebar, text="📌 Bảng điều khiển", command=self.show_dashboard, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="📤 Nộp bài tập", command=self.show_assignment, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="📝 Đăng ký học phần", command=self.show_register, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="📈 Tra cứu điểm", command=self.show_grades, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="🔑 Điểm danh OTP", command=self.show_attendance, **btn_opts).pack(fill="x", padx=15, pady=5)

        # NÚT THEME
        self.btn_theme = ctk.CTkButton(self.sidebar, text="☀️ Light Mode" if ctk.get_appearance_mode()=="Dark" else "🌙 Dark Mode", 
                                       command=self.toggle_theme, fg_color=("gray85", "#2C2C2E"), text_color=("black", "white"), font=("Segoe UI", 12, "bold"), corner_radius=20)
        self.btn_theme.pack(side="bottom", fill="x", padx=20, pady=(0, 25))

        # PROFILE BADGE
        user = main_controller.current_user
        u_name = getattr(user, 'name', 'Hoàng Việt Anh')
        u_id = getattr(user, 'user_id', '25112007')
        initials = "".join([w[0] for w in u_name.split()[-2:]]).upper() if len(u_name.split()) >= 2 else u_name[:2].upper()

        self.profile_card = ctk.CTkFrame(self.sidebar, corner_radius=15, fg_color=("gray85", "#2C2C2E"))
        self.profile_card.pack(side="bottom", fill="x", padx=15, pady=(0, 20))
        self.avatar = ctk.CTkLabel(self.profile_card, text=initials, font=("Segoe UI", 16, "bold"), 
                                   width=46, height=46, corner_radius=23, fg_color="#10B981", text_color="white") # Avatar xanh Sinh Viên
        self.avatar.pack(side="left", padx=10, pady=10)

        info_f = ctk.CTkFrame(self.profile_card, fg_color="transparent")
        info_f.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(info_f, text=u_name, font=("Segoe UI", 13, "bold"), text_color=("black", "white"), anchor="w").pack(fill="x")
        ctk.CTkLabel(info_f, text=f"UID: {u_id}", font=("Consolas", 11), text_color=("gray40", "gray60"), anchor="w").pack(fill="x")

        # MAIN CONTAINER
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)

        action_btn = {"font": ("Segoe UI", 13, "bold"), "height": 45, "corner_radius": 22, "cursor": "hand2"}
        entry_opts = {"height": 45, "font": ("Segoe UI", 14), "border_width": 0, "corner_radius": 10, "fg_color": ("#F3F4F6", "#2C2C2E")}

        # 1. DASHBOARD
        self.frame_dashboard = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_dashboard, text="Tổng quan & Thông báo học vụ", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        self.info_frame = ctk.CTkFrame(self.frame_dashboard, corner_radius=15, fg_color=CARD_BG)
        self.info_frame.pack(fill="x", pady=10, ipadx=20, ipady=20)
        self.lbl_profile = ctk.CTkLabel(self.info_frame, text="Đang tải...", font=("Segoe UI", 15), text_color=("black", "white"))
        self.lbl_profile.pack(anchor="w")
        self.lbl_warning = ctk.CTkLabel(self.info_frame, text="", font=("Segoe UI", 15, "bold")); self.lbl_warning.pack(anchor="w", pady=8)
        ctk.CTkLabel(self.frame_dashboard, text="Hòm thư nhắc nhở:", font=("Segoe UI", 15, "bold"), text_color="#EF4444").pack(anchor="w", pady=(20, 10))
        self.list_notis = ctk.CTkTextbox(self.frame_dashboard, font=("Segoe UI", 14), corner_radius=15, text_color="#EF4444", fg_color=CARD_BG, padx=15, pady=15)
        self.list_notis.pack(fill="both", expand=True)

        # 2. BÀI TẬP
        self.frame_assignment = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_assignment, text="Nộp bài tập", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        ctk.CTkButton(self.frame_assignment, text="📤 Nộp bài tập đã chọn", fg_color="#3B82F6", hover_color="#2563EB", command=self.submit_hw, **action_btn).pack(anchor="w", pady=10)
        self.tree_hw = ttk.Treeview(self.frame_assignment, columns=('id', 'class', 'status', 'time'), show='headings')
        for col, text in zip(('id', 'class', 'status', 'time'), ('ID', 'Mã Lớp', 'Trạng thái', 'Thời gian nộp')): self.tree_hw.heading(col, text=text); self.tree_hw.column(col, anchor='center')
        self.tree_hw.pack(fill="both", expand=True)

        # 3. ĐĂNG KÝ
        self.frame_register = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_register, text="Đăng ký học phần", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        form_reg = ctk.CTkFrame(self.frame_register, corner_radius=15, fg_color=CARD_BG); form_reg.pack(fill="x", ipadx=25, ipady=30)
        self.entry_class_id = ctk.CTkEntry(form_reg, placeholder_text="Nhập mã lớp...", width=350, **entry_opts); self.entry_class_id.pack(pady=15)
        ctk.CTkButton(form_reg, text="Gửi Đăng Ký", fg_color="#10B981", hover_color="#059669", command=self.register, **action_btn).pack(pady=15)

        # 4. TRA CỨU ĐIỂM
        self.frame_grades = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_grades, text="Tra cứu điểm & GPA", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        self.lbl_scholarship = ctk.CTkLabel(self.frame_grades, text="", font=("Segoe UI", 15, "bold")); self.lbl_scholarship.pack(anchor="w", pady=10)
        self.tree_gr = ttk.Treeview(self.frame_grades, columns=('class', 'cc', 'gk', 'ck', 'tong', 'he4'), show='headings')
        for col, text in zip(('class', 'cc', 'gk', 'ck', 'tong', 'he4'), ('Mã Lớp', 'Chuyên cần', 'Giữa kỳ', 'Cuối kỳ', 'Tổng (10)', 'Hệ 4')): self.tree_gr.heading(col, text=text); self.tree_gr.column(col, anchor='center')
        self.tree_gr.pack(fill="both", expand=True)

        # 5. ĐIỂM DANH OTP
        self.frame_attendance = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_attendance, text="Điểm danh OTP", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        form_att = ctk.CTkFrame(self.frame_attendance, corner_radius=15, fg_color=CARD_BG); form_att.pack(fill="x", ipadx=25, ipady=30)
        self.entry_att_class = ctk.CTkEntry(form_att, placeholder_text="Mã lớp", width=350, **entry_opts); self.entry_att_class.pack(pady=15)
        self.entry_att_code = ctk.CTkEntry(form_att, placeholder_text="Mã bảo mật", font=("Segoe UI", 15, "bold"), text_color="#F59E0B", width=350, **entry_opts); self.entry_att_code.pack(pady=15)
        ctk.CTkButton(form_att, text="Check-in", fg_color="#F59E0B", hover_color="#D97706", command=self.handle_attendance, **action_btn).pack(pady=15)

        self.apply_treeview_style(ctk.get_appearance_mode())
        self.show_dashboard()
        self.window.mainloop()

    def toggle_theme(self):
        new_mode = "Light" if ctk.get_appearance_mode() == "Dark" else "Dark"
        ctk.set_appearance_mode(new_mode)
        self.apply_treeview_style(new_mode)
        self.btn_theme.configure(text="🌙 Dark Mode" if new_mode=="Light" else "☀️ Light Mode")

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

    def hide_all(self): self.frame_dashboard.pack_forget(); self.frame_assignment.pack_forget(); self.frame_register.pack_forget(); self.frame_grades.pack_forget(); self.frame_attendance.pack_forget()

    def show_dashboard(self):
        self.hide_all(); self.frame_dashboard.pack(fill="both", expand=True)
        info = self.student_ctr.get_dashboard_info()
        if info and "profile" in info:
            p = info["profile"]
            self.lbl_profile.configure(text=f"🎓 Tên: {p['name']}   |   🆔 UID: {p['uid']}   |   📈 GPA: {p['gpa']}   |   📚 TC: {p['credits']}")
            if info["warning"]["is_warned"]: self.lbl_warning.configure(text=f"⚠️ {info['warning']['message']}", text_color="#EF4444")
            else: self.lbl_warning.configure(text=f"✅ {info['warning']['message']}", text_color="#10B981")
        
        self.list_notis.configure(state="normal"); self.list_notis.delete("1.0", END)
        for n in self.student_ctr.get_notifications(): self.list_notis.insert(END, f"📢 [{n['time']}] {n['msg']}\n")
        self.list_notis.configure(state="disabled")

    def show_assignment(self):
        self.hide_all(); self.frame_assignment.pack(fill="both", expand=True)
        for row in self.tree_hw.get_children(): self.tree_hw.delete(row)
        for h in self.student_ctr.get_assignments(): self.tree_hw.insert('', 'end', values=(h['id'], h['class_id'], h['status'], h['time'] or "---"))

    def show_register(self): self.hide_all(); self.frame_register.pack(fill="both", expand=True)
    def show_grades(self):
        self.hide_all(); self.frame_grades.pack(fill="both", expand=True)
        for row in self.tree_gr.get_children(): self.tree_gr.delete(row)
        for g in self.student_ctr.get_detailed_grades(): self.tree_gr.insert('', 'end', values=(g['class_id'], g['cc'], g['gk'], g['ck'], g['tong'], g['he4']))
        info = self.student_ctr.get_dashboard_info()
        if info and info["profile"]['credits'] >= 18 and info["profile"]['gpa'] >= 3.2: self.lbl_scholarship.configure(text="🎉 Đủ ĐK học bổng!", text_color="#10B981")
        else: self.lbl_scholarship.configure(text="❌ Chưa đủ ĐK học bổng.", text_color="#EF4444")

    def show_attendance(self): self.hide_all(); self.frame_attendance.pack(fill="both", expand=True)

    def submit_hw(self):
        sel = self.tree_hw.selection()
        if sel and self.student_ctr.submit_assignment(int(self.tree_hw.item(sel[0])['values'][0]))[0]: self.show_assignment()

    def register(self):
        if self.student_ctr.register_class(self.entry_class_id.get().strip())[0]: messagebox.showinfo("OK", "Đăng ký thành công!")

    def handle_attendance(self):
        if self.student_ctr.check_in_attendance(self.entry_att_class.get().strip(), self.entry_att_code.get().strip())[0]: messagebox.showinfo("OK", "Điểm danh thành công!")

if __name__ == "__main__":
    fake_ctrl = MainController()
    # 💡 Cập nhật fake data để test avatar không bị lỗi
    fake_ctrl.current_user = type('obj', (object,), {'role': 'Student', 'name': 'Hoàng Việt Anh', 'user_id': '25112007'})() 
    StudentWindow(fake_ctrl)