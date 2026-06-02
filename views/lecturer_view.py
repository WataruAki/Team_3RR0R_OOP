import customtkinter as ctk
from tkinter import ttk, messagebox, END
import random, string
from controllers.controllers import LecturerController, MainController

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

APP_BG = ("#F3F4F6", "#000000")
CARD_BG = ("#FFFFFF", "#1C1C1E")

class LecturerWindow:
    def __init__(self, main_controller):
        self.lecturer_ctr = LecturerController(main_controller)
        self.window = ctk.CTk()
        self.window.geometry("1150x750")
        self.window.title("BCSE - Giảng Viên")
        self.window.configure(fg_color=APP_BG)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self.window, width=240, corner_radius=0, fg_color=CARD_BG)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        ctk.CTkLabel(self.sidebar, text="GIẢNG VIÊN", font=("Segoe UI", 24, "bold"), text_color="#06B6D4").pack(pady=(35, 30))
        btn_opts = {"fg_color": "transparent", "text_color": ("gray20", "gray80"), "hover_color": ("#E5E7EB", "#2C2C2E"), 
                    "font": ("Segoe UI", 14, "bold"), "anchor": "w", "height": 45, "corner_radius": 12}
        
        ctk.CTkButton(self.sidebar, text="📌 Lịch Giảng Dạy", command=self.show_dashboard, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="⏰ Mở Điểm Danh", command=self.show_attendance, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="💯 Quản lý Điểm", command=self.show_grade, **btn_opts).pack(fill="x", padx=15, pady=5)
        ctk.CTkButton(self.sidebar, text="📝 Track Bài Tập", command=self.show_assignment, **btn_opts).pack(fill="x", padx=15, pady=5)

        # NÚT THEME
        self.btn_theme = ctk.CTkButton(self.sidebar, text="☀️ Light Mode" if ctk.get_appearance_mode()=="Dark" else "🌙 Dark Mode", 
                                       command=self.toggle_theme, fg_color=("gray85", "#2C2C2E"), text_color=("black", "white"), font=("Segoe UI", 12, "bold"), corner_radius=20)
        self.btn_theme.pack(side="bottom", fill="x", padx=20, pady=(0, 25))

        # PROFILE BADGE
        user = main_controller.current_user
        u_name = getattr(user, 'name', 'Bùi Huy Kiên')
        u_id = getattr(user, 'user_id', 'VJU001')
        initials = "".join([w[0] for w in u_name.split()[-2:]]).upper() if len(u_name.split()) >= 2 else u_name[:2].upper()

        self.profile_card = ctk.CTkFrame(self.sidebar, corner_radius=15, fg_color=("gray85", "#2C2C2E"))
        self.profile_card.pack(side="bottom", fill="x", padx=15, pady=(0, 20))
        self.avatar = ctk.CTkLabel(self.profile_card, text=initials, font=("Segoe UI", 16, "bold"), 
                                   width=46, height=46, corner_radius=23, fg_color="#06B6D4", text_color="white")
        self.avatar.pack(side="left", padx=10, pady=10)

        info_f = ctk.CTkFrame(self.profile_card, fg_color="transparent")
        info_f.pack(side="left", fill="both", expand=True, pady=12)
        ctk.CTkLabel(info_f, text=u_name, font=("Segoe UI", 13, "bold"), text_color=("black", "white"), anchor="w").pack(fill="x")
        ctk.CTkLabel(info_f, text=f"UID: {u_id}", font=("Consolas", 11), text_color=("gray40", "gray60"), anchor="w").pack(fill="x")

        # MAIN CONTAINER
        self.main_frame = ctk.CTkFrame(self.window, fg_color="transparent")
        self.main_frame.pack(side="left", fill="both", expand=True, padx=25, pady=25)

        action_btn = {"font": ("Segoe UI", 13, "bold"), "height": 40, "corner_radius": 20, "cursor": "hand2"}
        entry_opts = {"height": 40, "font": ("Segoe UI", 13), "border_width": 0, "corner_radius": 8, "fg_color": ("#F3F4F6", "#2C2C2E")}

        # 1. DASHBOARD
        self.frame_dashboard = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_dashboard, text="Lớp Học Đang Phụ Trách", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        self.class_listbox = ctk.CTkTextbox(self.frame_dashboard, font=("Segoe UI", 15), corner_radius=15, fg_color=CARD_BG, padx=20, pady=20)
        self.class_listbox.pack(fill="both", expand=True)

        # 2. ĐIỂM DANH
        self.frame_attendance = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_attendance, text="Phiên Điểm Danh", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        form_att = ctk.CTkFrame(self.frame_attendance, corner_radius=15, fg_color=CARD_BG); form_att.pack(fill="x", ipadx=20, ipady=25)
        
        self.entry_att_class = ctk.CTkEntry(form_att, placeholder_text="Mã lớp học phần", width=320, **entry_opts); self.entry_att_class.pack(pady=10)
        
        otp_f = ctk.CTkFrame(form_att, fg_color="transparent"); otp_f.pack(pady=15)
        self.entry_att_token = ctk.CTkEntry(otp_f, placeholder_text="Mã OTP", font=("Segoe UI", 16, "bold"), width=160, height=45, border_width=0, corner_radius=8, fg_color=("white", "#333333"), text_color="#06B6D4")
        self.entry_att_token.pack(side="left", padx=(0, 15))
        ctk.CTkButton(otp_f, text="Tạo ngẫu nhiên", fg_color="#8B5CF6", hover_color="#7C3AED", **action_btn).pack(side="left")

        act_f = ctk.CTkFrame(form_att, fg_color="transparent"); act_f.pack(pady=15)
        ctk.CTkButton(act_f, text="▶ Mở phiên", fg_color="#10B981", hover_color="#059669", **action_btn).pack(side="left", padx=10)
        ctk.CTkButton(act_f, text="🔒 Đóng phiên", fg_color="#EF4444", hover_color="#DC2626", **action_btn).pack(side="left", padx=10)
        self.lbl_att_result = ctk.CTkLabel(form_att, text="", font=("Segoe UI", 13, "bold")); self.lbl_att_result.pack(pady=10)

        # 3. NHẬP ĐIỂM (CẬP NHẬT CÓ TREEVIEW)
        self.frame_grade = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_grade, text="Cập nhật Điểm & Khóa sổ", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        
        form_gr = ctk.CTkFrame(self.frame_grade, corner_radius=15, fg_color=CARD_BG); form_gr.pack(fill="x", ipadx=15, ipady=20)
        self.entry_grade_class = ctk.CTkEntry(form_gr, placeholder_text="Mã Lớp", width=140, **entry_opts); self.entry_grade_class.grid(row=0, column=0, padx=10, pady=10)
        self.entry_student = ctk.CTkEntry(form_gr, placeholder_text="Mã SV", width=140, **entry_opts); self.entry_student.grid(row=0, column=1, padx=10, pady=10)
        self.cmb_score = ctk.CTkComboBox(form_gr, values=["chuyen_can", "giua_ky", "cuoi_ky"], width=150, **entry_opts); self.cmb_score.grid(row=0, column=2, padx=10, pady=10)
        self.entry_score = ctk.CTkEntry(form_gr, placeholder_text="Điểm số", width=100, **entry_opts); self.entry_score.grid(row=0, column=3, padx=10, pady=10)
        ctk.CTkButton(form_gr, text="Lưu Điểm", fg_color="#3B82F6", hover_color="#2563EB", command=self.handle_input_grade, **action_btn).grid(row=0, column=4, padx=10, pady=10)
        self.lbl_grade_result = ctk.CTkLabel(form_gr, text="", font=("Segoe UI", 12)); self.lbl_grade_result.grid(row=1, column=0, columnspan=5)

        act_gr_f = ctk.CTkFrame(self.frame_grade, fg_color="transparent"); act_gr_f.pack(anchor="w", pady=(10, 20))
        # 💡 Bổ sung nút Tải Bảng Điểm
        ctk.CTkButton(act_gr_f, text="🔄 Tải Bảng Điểm", fg_color="#6B7280", hover_color="#4B5563", command=self.load_class_grades, **action_btn).pack(side="left", padx=(0, 15))
        ctk.CTkButton(act_gr_f, text="Tự động tính Điểm", fg_color="#8B5CF6", hover_color="#7C3AED", command=self.calculate_final, **action_btn).pack(side="left", padx=(0, 15))
        ctk.CTkButton(act_gr_f, text="Khóa điểm & Cập nhật GPA", fg_color="#EF4444", hover_color="#DC2626", command=self.lock_grades, **action_btn).pack(side="left")

        # 💡 Bổ sung Bảng dữ liệu Điểm
        self.tree_gr = ttk.Treeview(self.frame_grade, columns=('uid', 'name', 'cc', 'gk', 'ck', 'tong', 'he4'), show='headings')
        self.tree_gr.heading('uid', text='Mã SV'); self.tree_gr.heading('name', text='Họ và Tên')
        self.tree_gr.heading('cc', text='Chuyên cần'); self.tree_gr.heading('gk', text='Giữa kỳ'); self.tree_gr.heading('ck', text='Cuối kỳ')
        self.tree_gr.heading('tong', text='Tổng (10)'); self.tree_gr.heading('he4', text='Hệ 4')
        self.tree_gr.column('cc', width=90, anchor='center'); self.tree_gr.column('gk', width=90, anchor='center'); self.tree_gr.column('ck', width=90, anchor='center')
        self.tree_gr.column('tong', width=90, anchor='center'); self.tree_gr.column('he4', width=90, anchor='center')
        self.tree_gr.pack(fill="both", expand=True)
        self.tree_gr.bind("<ButtonRelease-1>", self.select_student_grade)

        # 4. TRACK BÀI TẬP
        self.frame_assignment = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        ctk.CTkLabel(self.frame_assignment, text="Phát Bài Tập", font=("Segoe UI", 26, "bold"), text_color=("black", "white")).pack(anchor="w", pady=(0, 20))
        tool_hw = ctk.CTkFrame(self.frame_assignment, fg_color="transparent"); tool_hw.pack(fill="x", pady=10)
        self.entry_hw_class = ctk.CTkEntry(tool_hw, placeholder_text="Mã lớp", width=180, **entry_opts); self.entry_hw_class.pack(side="left", padx=5)
        ctk.CTkButton(tool_hw, text="Giao bài mới", fg_color="#10B981", hover_color="#059669", **action_btn, command=self.create_hw).pack(side="left", padx=10)
        ctk.CTkButton(tool_hw, text="Tải danh sách", fg_color="#6B7280", hover_color="#4B5563", **action_btn, command=self.load_assignments).pack(side="left", padx=10)
        ctk.CTkButton(tool_hw, text="Nhắc nhở", fg_color="#F59E0B", hover_color="#D97706", **action_btn, command=self.send_reminder).pack(side="right", padx=5)

        self.tree_hw = ttk.Treeview(self.frame_assignment, columns=('uid', 'name', 'status', 'time'), show='headings'); self.tree_hw.heading('uid', text='Mã SV'); self.tree_hw.heading('name', text='Họ và Tên'); self.tree_hw.heading('status', text='Trạng thái'); self.tree_hw.heading('time', text='Thời gian nộp')
        self.tree_hw.pack(fill="both", expand=True, pady=10)

        self.apply_treeview_style(ctk.get_appearance_mode())
        self.show_dashboard()
        self.window.mainloop()

    # ==========================================
    # CẤU HÌNH GIAO DIỆN
    # ==========================================
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

    # ==========================================
    # LOGIC ĐIỀU HƯỚNG & NGHIỆP VỤ
    # ==========================================
    def hide_all_frames(self): self.frame_dashboard.pack_forget(); self.frame_attendance.pack_forget(); self.frame_grade.pack_forget(); self.frame_assignment.pack_forget()
    
    def show_dashboard(self):
        self.hide_all_frames(); self.frame_dashboard.pack(fill="both", expand=True); self.class_listbox.configure(state="normal"); self.class_listbox.delete("1.0", END)
        classes = self.lecturer_ctr.get_assigned_classes()
        if classes:
            for c in classes: self.class_listbox.insert(END, f"📌 Mã Lớp: {c['class_id']}  |  Môn: {c['course_id']}\n\n")
        else: self.class_listbox.insert(END, "Chưa được phân công.")
        self.class_listbox.configure(state="disabled")

    def show_attendance(self): self.hide_all_frames(); self.frame_attendance.pack(fill="both", expand=True)
    def show_grade(self): self.hide_all_frames(); self.frame_grade.pack(fill="both", expand=True)
    def show_assignment(self): self.hide_all_frames(); self.frame_assignment.pack(fill="both", expand=True)

    def generate_otp(self): self.entry_att_token.delete(0, END); self.entry_att_token.insert(0, ''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
    
    def handle_open_attendance(self):
        success, message = self.lecturer_ctr.open_attendance(self.entry_att_class.get().strip(), self.entry_att_token.get().strip())
        self.lbl_att_result.configure(text=message, text_color="#10B981" if success else "#EF4444")
        
    def handle_close_attendance(self):
        success, msg = self.lecturer_ctr.close_attendance(self.entry_att_class.get().strip())
        self.lbl_att_result.configure(text=msg, text_color="#3B82F6" if success else "#EF4444")

    # 💡 Logic Load Bảng Điểm
    def load_class_grades(self):
        cid = self.entry_grade_class.get().strip()
        if not cid:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng nhập Mã Lớp để xem điểm!")
            return
            
        for row in self.tree_gr.get_children(): self.tree_gr.delete(row)
        grades = self.lecturer_ctr.get_class_grades(cid) 
        if not grades:
            messagebox.showinfo("Thông báo", "Lớp này không có sinh viên hoặc mã lớp sai.")
            return
            
        for g in grades:
            self.tree_gr.insert('', 'end', values=(g['uid'], g['name'], g['cc'], g['gk'], g['ck'], g['tong'], g['he4']))

    # 💡 Auto Fill khi click vào tên Sinh viên trong bảng
    def select_student_grade(self, event):
        sel = self.tree_gr.selection()
        if sel:
            item = self.tree_gr.item(sel[0])['values']
            self.entry_student.delete(0, END)
            self.entry_student.insert(0, str(item[0])) # Lấy Mã SV (Cột đầu tiên)

    def handle_input_grade(self):
        try: value = float(self.entry_score.get())
        except: self.lbl_grade_result.configure(text="Điểm phải là số!", text_color="#EF4444"); return
        success, message = self.lecturer_ctr.input_grade(self.entry_grade_class.get().strip(), self.entry_student.get().strip(), self.cmb_score.get(), value)
        self.lbl_grade_result.configure(text=message, text_color="#10B981" if success else "#EF4444")
        if success: self.load_class_grades() # Tự động refresh bảng điểm

    def calculate_final(self):
        success, msg = self.lecturer_ctr.calculate_final_grades(self.entry_grade_class.get().strip())
        if success: 
            messagebox.showinfo("Hoàn tất", msg)
            self.load_class_grades() # Tự động refresh bảng điểm
        else: messagebox.showerror("Lỗi", msg)

    def lock_grades(self):
        cid = self.entry_grade_class.get().strip()
        if messagebox.askyesno("Khóa điểm", f"Khóa sổ {cid}? Lệnh này sẽ chốt điểm không cho sửa nữa."): 
            success, msg = self.lecturer_ctr.lock_class_grades(cid)
            if success: messagebox.showinfo("OK", msg)
            else: messagebox.showerror("Lỗi", msg)

    def create_hw(self):
        cid = self.entry_hw_class.get().strip()
        if cid and self.lecturer_ctr.create_assignment(cid)[0]: self.load_assignments()
        
    def load_assignments(self):
        for row in self.tree_hw.get_children(): self.tree_hw.delete(row)
        for item in self.lecturer_ctr.get_assignments(): self.tree_hw.insert('', 'end', values=(item['uid'], item['name'], item['status'], item['time']))
        
    def send_reminder(self): 
        success, msg = self.lecturer_ctr.send_assignment_reminders()
        if success: messagebox.showinfo("Thông báo", msg)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = type('obj', (object,), {'role': 'Lecturer', 'name': 'Bùi Huy Kiên', 'user_id': 'VJU001'})() 
    LecturerWindow(fake_ctrl)