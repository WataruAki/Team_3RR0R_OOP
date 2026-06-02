import os
from models.models import create_database, SessionLocal, User, Course, CourseClass, Enrollment, CompletedCourse, Assignment, Notification
from controllers.controllers import MainController, StudentController, LecturerController, AcademicStaffController, hash_pwd

def seed_mock_data():
    db = SessionLocal()
    try:
        if db.query(User).first(): return
        print("[SEED] Đang khởi tạo dữ liệu mẫu với Cấu trúc ID mới...")

        staff = User(user_id="001", name="Trần Thị Giáo Vụ", email="giaovu@vnu.edu.vn", password=hash_pwd("12345678", "giaovu@vnu.edu.vn"), role="Staff")
        lecturer = User(user_id="VJU001", name="Bùi Huy Kiên", email="giangvien@vnu.edu.vn", password=hash_pwd("12345678", "giangvien@vnu.edu.vn"), role="Lecturer")
        db.add_all([staff, lecturer])
        
        sv1 = User(user_id="25112007", name="Hoàng Việt Anh", email="anhhv@vnu.edu.vn", password=hash_pwd("12345678", "anhhv@vnu.edu.vn"), role="Student", gpa=3.8, rls=90, credits=21)
        sv2 = User(user_id="25112008", name="Lê Văn Thái An", email="anlv@vnu.edu.vn", password=hash_pwd("12345678", "anlv@vnu.edu.vn"), role="Student", gpa=3.5, rls=85, credits=18)
        sv3 = User(user_id="25112009", name="Nguyễn Vũ Hương Ly", email="lynv@vnu.edu.vn", password=hash_pwd("12345678", "lynv@vnu.edu.vn"), role="Student", gpa=2.9, rls=75, credits=15)
        
        # THÊM SINH VIÊN CÁ BIỆT ĐỂ TEST CẢNH CÁO HỌC VỤ
        sv_fail = User(user_id="25112010", name="Nguyễn Cá Biệt", email="cabiet@vnu.edu.vn", password=hash_pwd("12345678", "cabiet@vnu.edu.vn"), role="Student", gpa=1.5, rls=40, credits=10)
        
        db.add_all([sv1, sv2, sv3, sv_fail])
        db.commit()

        mon_oop = Course(course_id="CSE3011", course_name="Lập trình hướng đối tượng", credits=3)
        mon_ml = Course(course_id="CSE4022", course_name="Nhập môn Học máy", credits=3, prerequisite_id="CSE3011")
        mon_web = Course(course_id="WEB2011", course_name="Phát triển Ứng dụng Web", credits=3)
        db.add_all([mon_oop, mon_ml, mon_web])
        db.commit()

        lop_oop_1 = CourseClass(class_id="CSE3011_C1", course_id="CSE3011", lecturer_id="VJU001",max_capacity=2)
        lop_oop_2 = CourseClass(class_id="CSE3011_C2", course_id="CSE3011", lecturer_id="VJU001")
        lop_web = CourseClass(class_id="WEB2011_C1", course_id="WEB2011", lecturer_id="VJU001")
        db.add_all([lop_oop_1, lop_oop_2, lop_web])
        db.commit()

        en1 = Enrollment(class_id="CSE3011_C1", student_id="25112007", chuyen_can=8.0, giua_ky=9.0, cuoi_ky=9.5)
        en2 = Enrollment(class_id="CSE3011_C1", student_id="25112008", chuyen_can=9.0, giua_ky=8.0, cuoi_ky=8.0)
        
        bt1 = Assignment(class_id="CSE3011_C1", student_id="25112007", status="Chưa nộp") 
        bt2 = Assignment(class_id="CSE3011_C1", student_id="25112008", status="Chưa nộp") 

        db.add_all([bt1, bt2, en1, en2])
        db.commit()
        
        print("[SEED] Nạp dữ liệu mô phỏng thành công.\n")
    except Exception as e:
        db.rollback()
        print(f"[SEED] Lỗi nghiêm trọng khi nạp dữ liệu: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_database()
    seed_mock_data()