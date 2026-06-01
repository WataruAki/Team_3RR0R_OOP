import os
from models.models import create_database, SessionLocal, User, Course, CourseClass, Enrollment, CompletedCourse, Assignment, Project
from controllers.controllers import MainController, StudentController, LecturerController, AcademicStaffController

def seed_mock_data():
    db = SessionLocal()
    try:
        if db.query(User).first():
            return

        print("[SEED] Đang khởi tạo dữ liệu mẫu cho hệ thống...")

        # Thêm mật khẩu password="123" cho tài khoản mẫu
        staff = User(user_id="1", name="Trần Thị Giáo Vụ", email="giaovu@vnu.edu.vn", password="123", role="Staff")
        lecturer = User(user_id="2", name="Nguyễn Văn Giảng Viên", email="giangvien@vnu.edu.vn", password="123", role="Lecturer")
        db.add_all([staff, lecturer])
        db.commit()

        sv1 = User(user_id="3", name="Hoàng Việt Anh", email="anhhv@vnu.edu.vn", password="123", role="Student", gpa=3.8, rls=90, credits=21, attendance_rate=1.0)
        sv2 = User(user_id="4", name="Lê Văn Thái An", email="anlv@vnu.edu.vn", password="123", role="Student", gpa=3.5, rls=85, credits=18, attendance_rate=0.95)
        sv3 = User(user_id="5", name="Nguyễn Vũ Hương Ly", email="lynv@vnu.edu.vn", password="123", role="Student", gpa=2.9, rls=75, credits=15, attendance_rate=0.85)
        sv4 = User(user_id="6", name="Hoàng Phương Đông Hòa", email="hoahpd@vnu.edu.vn", password="123", role="Student", gpa=3.1, rls=82, credits=19, attendance_rate=0.9)
        sv_fail = User(user_id="7", name="Nguyễn Cá Biệt", email="cabiet@vnu.edu.vn", password="123", role="Student", gpa=2.2, rls=50, credits=12, attendance_rate=0.7)
        db.add_all([sv1, sv2, sv3, sv4, sv_fail])
        db.commit()

        mon_oop = Course(course_id="INT2204", course_name="Lập trình hướng đối tượng", credits=3)
        mon_adv = Course(course_id="INT3301", course_name="Phần mềm nâng cao", credits=3, prerequisite_id="INT2204")
        db.add_all([mon_oop, mon_adv])
        db.commit()

        lop_oop = CourseClass(class_id="L01_C1", course_id="INT2204", lecturer_id="2")
        db.add(lop_oop)
        db.commit()

        en1 = Enrollment(class_id="L01_C1", student_id="3", chuyen_can=8.0, giua_ky=9.0, cuoi_ky=9.5)
        en2 = Enrollment(class_id="L01_C1", student_id="4", chuyen_can=9.0, giua_ky=8.0, cuoi_ky=8.0)
        en_fail = Enrollment(class_id="L01_C1", student_id="7", chuyen_can=5.0, giua_ky=4.0, cuoi_ky=3.0)

        # TẠO DỮ LIỆU BÀI TẬP MẪU
        bt1 = Assignment(class_id="L01_C1", student_id="3", status="Chưa nộp") # ID 3 là Việt Anh
        bt2 = Assignment(class_id="L01_C1", student_id="4", status="Chưa nộp") # ID 4 là Thái An
        bt3 = Assignment(class_id="L01_C1", student_id="7", status="Đã nộp", submit_time="01/06/2026 08:30") # ID 7 là Cá Biệt

        db.add_all([bt1, bt2, bt3])
        
        # db.commit() <--- Chèn ngay trên dòng commit lưu dữ liệu này
        db.add_all([en1, en2, en_fail])
        db.commit()
        
        print("[SEED] Nạp dữ liệu mô phỏng thành công.\n")
    except Exception as e:
        db.rollback()
        print(f"[SEED] Lỗi nghiêm trọng khi nạp dữ liệu: {e}")
    finally:
        db.close()



def run_system_simulation():
    print("="*60)
    print(" 🚀 KHỞI CHẠY KỊCH BẢN KIỂM THỬ HỆ THỐNG QUẢN LÝ HỌC VỤ")
    print("="*60)

    main_ctrl = MainController()
    student_ctrl = StudentController(main_ctrl)
    lecturer_ctrl = LecturerController(main_ctrl)
    staff_ctrl = AcademicStaffController(main_ctrl)

    print("\n▶ [GIÁO VỤ] Đăng nhập và quản trị")
    success, msg, role = main_ctrl.login("giaovu@vnu.edu.vn", "123")
    print(f"[-] {msg} (Role: {role})")

    print("\n▶ [GIẢNG VIÊN] Mở phiên điểm danh")
    main_ctrl.login("giangvien@vnu.edu.vn", "123")
    success, msg = lecturer_ctrl.open_attendance("L01_C1", "OOP_2026")
    print(f"[-] {msg}")

    print("\n▶ [SINH VIÊN] Trải nghiệm học vụ")
    main_ctrl.login("anhhv@vnu.edu.vn", "123")
    dash = student_ctrl.get_dashboard_info()
    print(f"[-] Dashboard ({dash['profile']['name']}): {dash['warning']['message']}")

    print("\n" + "="*60)
    print(" ✅ KẾT THÚC KIỂM THỬ - HỆ THỐNG ỔN ĐỊNH")
    print("="*60)

    print("\n▶ [TC03] KIỂM THỬ XUYÊN QUYỀN (AUTHORIZATION BYPASS)")
    
    # 1. Sinh viên Việt Anh đăng nhập hợp lệ
    main_ctrl.login("anhhv@vnu.edu.vn", "123")
    
    # 2. Sinh viên này am hiểu IT, cố tình gọi thẳng Controller của Giáo vụ
    # để xem lén danh sách xét học bổng của toàn khoa
    try:
        du_lieu_bi_lo = staff_ctrl.execute_scholarship_filter(2)
        print(f"[!] LỖ HỔNG BẢO MẬT: Sinh viên đã lấy được dữ liệu: {du_lieu_bi_lo}")
    except Exception as e:
        print(f"[-] Hệ thống đã chặn thành công: {e}")

if __name__ == "__main__":
    create_database()
    seed_mock_data()
    run_system_simulation()