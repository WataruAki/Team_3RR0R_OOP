import os
from models.models import create_database, SessionLocal, User, Course, CourseClass, Enrollment, CompletedCourse
from controllers.controllers import MainController, StudentController, LecturerController, AcademicStaffController

def seed_mock_data():
    """Hàm nạp dữ liệu mẫu ban đầu vào cơ sở dữ liệu SQLite"""
    db = SessionLocal()
    try:
        # Tránh nạp đúp dữ liệu nếu đã có sẵn
        if db.query(User).first():
            return

        print("[SEED] Đang khởi tạo dữ liệu mẫu cho hệ thống...")

        # 1. Thêm Giáo vụ & Giảng viên
        staff = User(name="Trần Thị Giáo Vụ", email="giaovu@vnu.edu.vn", role="Staff")
        lecturer = User(name="Nguyễn Văn Giảng Viên", email="giangvien@vnu.edu.vn", role="Lecturer")
        db.add_all([staff, lecturer])
        db.commit() # Lưu để lấy uid

        # 2. Thêm Sinh viên (Nhóm 3RROR và 1 sinh viên cá biệt)
        sv1 = User(name="Hoàng Việt Anh", email="anhhv@vnu.edu.vn", role="Student", gpa=3.8, rls=90, credits=21, attendance_rate=1.0)
        sv2 = User(name="Lê Văn Thái An", email="anlv@vnu.edu.vn", role="Student", gpa=3.5, rls=85, credits=18, attendance_rate=0.95)
        sv3 = User(name="Nguyễn Vũ Hương Ly", email="lynv@vnu.edu.vn", role="Student", gpa=2.9, rls=75, credits=15, attendance_rate=0.85)
        sv4 = User(name="Hoàng Phương Đông Hòa", email="hoahpd@vnu.edu.vn", role="Student", gpa=3.1, rls=82, credits=19, attendance_rate=0.9)
        sv_fail = User(name="Nguyễn Cá Biệt", email="cabiet@vnu.edu.vn", role="Student", gpa=2.2, rls=50, credits=12, attendance_rate=0.7)
        db.add_all([sv1, sv2, sv3, sv4, sv_fail])
        db.commit()

        # 3. Thêm Môn học & Lớp học phần
        mon_oop = Course(course_id="INT2204", course_name="Lập trình hướng đối tượng", credits=3)
        mon_adv = Course(course_id="INT3301", course_name="Phần mềm nâng cao", credits=3, prerequisite_id="INT2204")
        db.add_all([mon_oop, mon_adv])
        db.commit()

        # Giảng viên (uid=2) mở lớp OOP
        lop_oop = CourseClass(class_id="L01_C1", course_id="INT2204", lecturer_id=2)
        db.add(lop_oop)
        db.commit()

        # 4. Ghi danh sinh viên vào lớp
        # sv1 (uid=3), sv2 (uid=4), sv_fail (uid=7)
        en1 = Enrollment(class_id="L01_C1", student_id=3, chuyen_can=8.0, giua_ky=9.0, cuoi_ky=9.5)
        en2 = Enrollment(class_id="L01_C1", student_id=4, chuyen_can=9.0, giua_ky=8.0, cuoi_ky=8.0)
        en_fail = Enrollment(class_id="L01_C1", student_id=7, chuyen_can=5.0, giua_ky=4.0, cuoi_ky=3.0)
        db.add_all([en1, en2, en_fail])
        db.commit()
        
        print("[SEED] Nạp dữ liệu mô phỏng thành công.\n")
    except Exception as e:
        db.rollback()
        print(f"[SEED] Thất bại: {e}")
    finally:
        db.close()


def run_system_simulation():
    """Hàm mô phỏng kịch bản chạy thử nghiệm hệ thống"""
    print("="*60)
    print(" 🚀 KHỞI CHẠY KỊCH BẢN KIỂM THỬ HỆ THỐNG QUẢN LÝ HỌC VỤ")
    print("="*60)

    main_ctrl = MainController()
    student_ctrl = StudentController(main_ctrl)
    lecturer_ctrl = LecturerController(main_ctrl)
    staff_ctrl = AcademicStaffController(main_ctrl)

    # -------------------------------------------------------------
    # 1. KỊCH BẢN GIÁO VỤ: XÉT HỌC BỔNG & THỐNG KÊ (USE CASE 1 & 5)
    # -------------------------------------------------------------
    print("\n▶ [GIÁO VỤ] Đăng nhập và quản trị")
    success, msg, role = main_ctrl.login("giaovu@vnu.edu.vn")
    print(f"[-] {msg} (Role: {role})")

    print("[-] Đang chạy Engine Xét học bổng (Chỉ tiêu: 2 suất)...")
    winners = staff_ctrl.execute_scholarship_filter(slots=2)
    for i, w in enumerate(winners, 1):
        print(f"    🏆 Top {i}: {w['name']} - Điểm xét tuyển: {w['score']:.2f}")

    chart_data = staff_ctrl.load_pie_chart_data()
    print(f"[-] Dữ liệu vẽ biểu đồ tròn (Pie Chart): {chart_data}")


    # -------------------------------------------------------------
    # 2. KỊCH BẢN GIẢNG VIÊN: MỞ ĐIỂM DANH (USE CASE 3)
    # -------------------------------------------------------------
    print("\n▶ [GIẢNG VIÊN] Mở phiên điểm danh")
    main_ctrl.login("giangvien@vnu.edu.vn")
    
    success, msg = lecturer_ctrl.open_attendance("L01_C1", "OOP_2026")
    print(f"[-] {msg}")


    # -------------------------------------------------------------
    # 3. KỊCH BẢN SINH VIÊN: CẢNH BÁO, ĐIỂM DANH, ĐĂNG KÝ (USE CASES 2, 3, 4)
    # -------------------------------------------------------------
    print("\n▶ [SINH VIÊN] Trải nghiệm học vụ")
    
    # 3.1 Sinh viên Việt Anh đăng nhập
    main_ctrl.login("anhhv@vnu.edu.vn")
    dash = student_ctrl.get_dashboard_info()
    print(f"[-] Dashboard ({dash['profile']['name']}): {dash['warning']['message']}")
    
    # Check-in điểm danh portal
    _, checkin_msg = student_ctrl.check_in_attendance("L01_C1", "OOP_2026")
    print(f"[-] Điểm danh: {checkin_msg}")

    # Đăng ký môn nâng cao (bị chặn do chưa có điểm môn OOP)
    _, reg_msg = student_ctrl.register_class("INT3301")
    print(f"[-] Đăng ký học phần: {reg_msg}")

    # 3.2 Sinh viên cá biệt đăng nhập (Test cảnh báo)
    main_ctrl.login("cabiet@vnu.edu.vn")
    dash_fail = student_ctrl.get_dashboard_info()
    print(f"[!] Dashboard ({dash_fail['profile']['name']}): {dash_fail['warning']['message']}")

    print("\n" + "="*60)
    print(" ✅ KẾT THÚC KIỂM THỬ - HỆ THỐNG ỔN ĐỊNH")
    print("="*60)


if __name__ == "__main__":
    # 1. Khởi tạo Database (Tạo file hms_database.db)
    create_database()
    
    # 2. Nạp dữ liệu giả lập
    seed_mock_data()
    
    # 3. Chạy kịch bản
    run_system_simulation()