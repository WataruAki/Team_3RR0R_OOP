from tkinter import *
from tkinter import ttk
from controllers import AcademicStaffController, MainController

class ASWindow:
    def __init__(self, main_controller):
        self.as_ctr = AcademicStaffController(main_controller)

        self.window = Tk()
        self.window.geometry("1920x1080")
        self.window.title("BCSE - Giáo Vụ")

        # Sidebar
        self.sidebar = Frame(self.window, width=200, bg="white", bd=1, relief="solid")
        self.sidebar.pack(side="left", fill="y", padx=(20,0), pady=20)
        self.sidebar.pack_propagate(False)

        Label(self.sidebar, text="Giáo vụ", font=("Segoe UI", 13, "bold"), bg="white").pack(pady=(20,30))
        Button(self.sidebar, text="Xét học bổng", command=self.show_scholarship).pack(fill="x", pady=5)
        Button(self.sidebar, text="Thống kê GPA", command=self.show_stats).pack(fill="x", pady=5)

        # Main frame
        self.main_frame = Frame(self.window, bg="#f0f4f8")
        self.main_frame.pack(side="left", fill="both", expand=True)

        # Frame học bổng
        self.frame_scholarship = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_scholarship, text="Xét học bổng", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Label(self.frame_scholarship, text="Số suất học bổng", font=("Segoe UI", 11, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30)
        self.entry_slots = Entry(self.frame_scholarship, font=("Segoe UI", 13), width=10)
        self.entry_slots.pack(anchor="w", padx=30, pady=(0,10))
        Button(self.frame_scholarship, text="Xét duyệt",
               command=self.handle_scholarship).pack(anchor="w", padx=30)
        self.lbl_scholarship_err = Label(self.frame_scholarship, text="", fg="red", bg="#f0f4f8")
        self.lbl_scholarship_err.pack(anchor="w", padx=30, pady=5)

        # Bảng kết quả học bổng
        cols = ("STT", "Mã SV", "Họ tên", "Điểm xét")
        self.table = ttk.Treeview(self.frame_scholarship, columns=cols, show="headings", height=15)
        for col in cols:
            self.table.heading(col, text=col)
            self.table.column(col, anchor="center", width=150)
        self.table.pack(padx=30, pady=10, anchor="w")

        # Frame thống kê
        self.frame_stats = Frame(self.main_frame, bg="#f0f4f8")
        Label(self.frame_stats, text="Thống kê GPA", font=("Segoe UI", 16, "bold"),
              bg="#f0f4f8").pack(anchor="w", padx=30, pady=20)
        Button(self.frame_stats, text="Tải dữ liệu",
               command=self.handle_load_stats).pack(anchor="w", padx=30)

        # Bảng thống kê
        cols2 = ("Xếp loại", "Số sinh viên")
        self.table_stats = ttk.Treeview(self.frame_stats, columns=cols2, show="headings", height=6)
        for col in cols2:
            self.table_stats.heading(col, text=col)
            self.table_stats.column(col, anchor="center", width=200)
        self.table_stats.pack(padx=30, pady=10, anchor="w")

        self.show_scholarship()
        self.window.mainloop()

    def handle_scholarship(self):
        try:
            slots = int(self.entry_slots.get())
        except ValueError:
            self.lbl_scholarship_err.config(text="Số suất phải là số nguyên.")
            return
        self.lbl_scholarship_err.config(text="")

        winners = self.as_ctr.execute_scholarship_filter(slots)

        self.table.delete(*self.table.get_children())
        if not winners:
            self.lbl_scholarship_err.config(text="Không có sinh viên đủ điều kiện.", fg="orange")
            return
        for i, w in enumerate(winners, 1):
            self.table.insert("", "end", values=(i, w["uid"], w["name"], f"{w['score']:.2f}"))

    def handle_load_stats(self):
        stats = self.as_ctr.load_pie_chart_data()
        self.table_stats.delete(*self.table_stats.get_children())
        for xep_loai, so_luong in stats.items():
            self.table_stats.insert("", "end", values=(xep_loai, so_luong))

    def show_scholarship(self):
        self.frame_stats.pack_forget()
        self.frame_scholarship.pack(fill="both", expand=True)

    def show_stats(self):
        self.frame_scholarship.pack_forget()
        self.frame_stats.pack(fill="both", expand=True)

if __name__ == "__main__":
    fake_ctrl = MainController()
    fake_ctrl.current_user = None
    ASWindow(fake_ctrl)