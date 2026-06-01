from models.models import SessionLocal, User, Course, CourseClass, Enrollment, Project, CompletedCourse, Assignment, Notification
import csv
from datetime import datetime
import hashlib

def hash_pwd(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

class MainController:
    def __init__(self):
        self.current_user = None

    def login(self, email: str, password: str) -> tuple[bool, str, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user or user.password != hash_pwd(password):
                return False, "Email hoặc Mật khẩu không chính xác", ""
            
            # VÁ LỖ HỔNG 2: CHẶN ĐĂNG NHẬP KHI BỊ ĐÌNH CHỈ HỌC
            if user.role == "Student" and user.academic_status == "Đình chỉ học":
                return False, "Tài khoản đã bị ĐÌNH CHỈ HỌC VỤ. Vui lòng liên hệ Giáo vụ!", ""
                
            self.current_user = user
            return True, f"Chào mừng {user.name} quay trở lại!", user.role
        finally:
            db.close()

    def logout(self):
        self.current_user = None

class StudentController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def get_dashboard_info(self) -> dict:
        if not self.main_ctrl.current_user: return {"profile": {}, "warning": {}, "classes": []}
        db = SessionLocal()
        try:
            student = db.query(User).filter(User.user_id == self.main_ctrl.current_user.user_id).first()
            is_warned = student.gpa < 2.8 or student.attendance_rate < 0.8
            warn_msg = "Cảnh báo: Vi phạm chuẩn đầu ra!" if is_warned else "Trạng thái học tập bình thường."

            enrollments = db.query(Enrollment).filter(Enrollment.student_id == student.user_id).all()
            classes_info = [{"class_id": en.class_id, "chuyen_can": en.chuyen_can, "giua_ky": en.giua_ky, "cuoi_ky": en.cuoi_ky} for en in enrollments]
            return {
                "profile": {"name": student.name, "uid": student.user_id, "gpa": student.gpa, "credits": student.credits},
                "warning": {"is_warned": is_warned, "message": warn_msg},
                "classes": classes_info
            }
        finally:
            db.close()

    def register_class(self, class_id: str) -> tuple[bool, str]:
        if not self.main_ctrl.current_user: return False, "Lỗi: Chưa đăng nhập."
        db = SessionLocal()
        try:
            student_id = self.main_ctrl.current_user.user_id
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id).first()
            if not course_class: return False, "Lớp học phần không tồn tại."

            current_enrolled = db.query(Enrollment).filter(Enrollment.class_id == class_id).count()
            if current_enrolled >= course_class.max_capacity:
                return False, "Bị chặn: Lớp đã đạt giới hạn sĩ số!"

            course = db.query(Course).filter(Course.course_id == course_class.course_id).first()
            
            # VÁ LỖ HỔNG 4: CHẶN ĐĂNG KÝ HỌC LẠI MÔN ĐÃ QUA
            passed = db.query(CompletedCourse).filter(CompletedCourse.student_id == student_id, CompletedCourse.course_id == course.course_id, CompletedCourse.grade_letter != 'F').first()
            if passed: return False, f"Bị chặn: Bạn đã học qua và ĐỖ môn này rồi ({passed.grade_letter})!"

            if course.prerequisite_id:
                completed = db.query(CompletedCourse).filter(CompletedCourse.student_id == student_id, CompletedCourse.course_id == course.prerequisite_id).first()
                if not completed or completed.grade_letter == 'F':
                    return False, f"Bị chặn: Chưa hoàn thành môn tiên quyết {course.prerequisite_id}!"

            if db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first():
                return False, "Bạn đã đăng ký lớp học phần này rồi."

            new_en = Enrollment(class_id=class_id, student_id=student_id)
            db.add(new_en)
            db.commit()
            return True, f"Đăng ký thành công lớp {class_id}."
        finally:
            db.close()

    def check_in_attendance(self, class_id: str, code: str) -> tuple[bool, str]:
        if not self.main_ctrl.current_user: return False, "Lỗi: Chưa đăng nhập."
        db = SessionLocal()
        try:
            student_id = self.main_ctrl.current_user.user_id
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id).first()
            if not course_class or course_class.attendance_code != code:
                return False, "Mã không hợp lệ hoặc phiên đã đóng."

            enrollment = db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first()
            if not enrollment: return False, "Bạn không có trong danh sách."
            
            if enrollment.last_otp == code:
                return False, "⛔ Bạn ĐÃ ĐIỂM DANH trong phiên này rồi! Không thể gian lận."

            enrollment.chuyen_can = min(10.0, enrollment.chuyen_can + 1.0)
            enrollment.last_otp = code
            db.commit()
            return True, "Xác nhận điểm danh thành công!"
        finally:
            db.close()

    def get_notifications(self) -> list:
        db = SessionLocal()
        try:
            notis = db.query(Notification).filter(Notification.user_id == self.main_ctrl.current_user.user_id).all()
            return [{"msg": n.message, "time": n.created_at} for n in notis]
        finally:
            db.close()

    def get_assignments(self) -> list:
        db = SessionLocal()
        try:
            hws = db.query(Assignment).filter(Assignment.student_id == self.main_ctrl.current_user.user_id).all()
            return [{"id": a.id, "class_id": a.class_id, "status": a.status, "time": a.submit_time} for a in hws]
        finally:
            db.close()

    def submit_assignment(self, assignment_id: int) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            hw = db.query(Assignment).filter(Assignment.id == assignment_id, Assignment.student_id == self.main_ctrl.current_user.user_id).first()
            if not hw: return False, "Không tìm thấy bài tập hoặc bạn không có quyền."
            if hw.status == "Đã nộp": return False, "Bạn đã nộp bài này rồi!"
            hw.status = "Đã nộp"
            hw.submit_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            db.commit()
            return True, "Nộp bài thành công!"
        finally:
            db.close()

    def get_detailed_grades(self) -> list:
        db = SessionLocal()
        try:
            enrollments = db.query(Enrollment).filter(Enrollment.student_id == self.main_ctrl.current_user.user_id).all()
            return [{"class_id": e.class_id, "cc": e.chuyen_can, "gk": e.giua_ky, "ck": e.cuoi_ky, "tong": e.diem_tong_ket, "he4": e.diem_he_4} for e in enrollments]
        finally:
            db.close()

class LecturerController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def get_assigned_classes(self) -> list:
        if not self.main_ctrl.current_user: return []
        db = SessionLocal()
        try:
            classes = db.query(CourseClass).filter(CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).all()
            return [{"class_id": c.class_id, "course_id": c.course_id} for c in classes]
        finally:
            db.close()

    def open_attendance(self, class_id: str, token_code: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Bạn không phụ trách lớp này."
            course_class.attendance_code = token_code
            db.commit()
            return True, f"Mở phiên điểm danh lớp {class_id} với mã: {token_code}"
        finally:
            db.close()

    def close_attendance(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Lớp không tồn tại."
            course_class.attendance_code = None
            db.commit()
            return True, f"Đã đóng phiên điểm danh lớp {class_id}."
        finally:
            db.close()

    def input_grade(self, class_id: str, student_id: str, score_type: str, value: float) -> tuple[bool, str]:
        if not (0.0 <= value <= 10.0): return False, "Lỗi: Điểm số phải từ 0.0 đến 10.0!"
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Bạn không phụ trách lớp này."
            enrollment = db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first()
            if not enrollment: return False, "Sinh viên không nằm trong danh sách."
            if enrollment.is_locked: return False, "Bảng điểm đã bị khóa!"

            if score_type == 'chuyen_can': enrollment.chuyen_can = value
            elif score_type == 'giua_ky': enrollment.giua_ky = value
            elif score_type == 'cuoi_ky': enrollment.cuoi_ky = value
            db.commit()
            return True, f"Cập nhật điểm {score_type} thành công."
        finally:
            db.close()
        
    def calculate_final_grades(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Lỗi: Bạn không phụ trách lớp này!"
            
            enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()
            if not enrollments: return False, "Lớp chưa có sinh viên."
            for e in enrollments:
                tong = (e.chuyen_can * 0.1) + (e.giua_ky * 0.2) + (e.cuoi_ky * 0.7)
                e.diem_tong_ket = round(tong, 2)
                if tong >= 8.5: e.diem_he_4 = 4.0
                elif tong >= 7.0: e.diem_he_4 = 3.0
                elif tong >= 5.5: e.diem_he_4 = 2.0
                elif tong >= 4.0: e.diem_he_4 = 1.0
                else: e.diem_he_4 = 0.0
            db.commit()
            return True, f"Tính điểm tổng kết thành công cho {len(enrollments)} SV."
        finally:
            db.close()

    def lock_class_grades(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Lỗi: Bạn không phụ trách lớp này!"
            
            enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()
            if not enrollments: return False, "Lớp không có dữ liệu."
            
            course_credits = course_class.course.credits if course_class.course else 0
            count = 0
            for e in enrollments:
                if not e.is_locked:
                    e.is_locked = True
                    student = db.query(User).filter(User.user_id == e.student_id).first()
                    
                    # Cập nhật GPA
                    if student and e.diem_he_4 is not None:
                        total_score = (student.gpa * student.credits) + (e.diem_he_4 * course_credits)
                        new_credits = student.credits + course_credits
                        if new_credits > 0: 
                            student.gpa = round(total_score / new_credits, 2)
                        student.credits = new_credits
                        
                        # VÁ LỖ HỔNG 1 (HỐ ĐEN TIÊN QUYẾT): Đẩy dữ liệu sang bảng CompletedCourse
                        letter = "A" if e.diem_he_4 == 4.0 else ("B" if e.diem_he_4 == 3.0 else ("C" if e.diem_he_4 == 2.0 else ("D" if e.diem_he_4 == 1.0 else "F")))
                        passed_record = db.query(CompletedCourse).filter_by(student_id=student.user_id, course_id=course_class.course_id).first()
                        if not passed_record:
                            db.add(CompletedCourse(student_id=student.user_id, course_id=course_class.course_id, grade_letter=letter))
                        else:
                            passed_record.grade_letter = letter
                    count += 1
            db.commit()
            return True, f"🔒 Đã khóa sổ và cập nhật GPA chính thức cho {count} sinh viên!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khóa điểm: {str(e)}"
        finally:
            db.close()

    def create_assignment(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id, CourseClass.lecturer_id == self.main_ctrl.current_user.user_id).first()
            if not course_class: return False, "Bạn không phụ trách lớp này."
            
            # VÁ LỖ HỔNG 3: CHẶN SPAM TẠO BÀI TẬP TRÙNG LẶP
            exist_hw = db.query(Assignment).filter(Assignment.class_id == class_id).first()
            if exist_hw: return False, f"⛔ Lớp {class_id} ĐÃ ĐƯỢC GIAO BÀI rồi! Không thể giao trùng lặp."
            
            enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()
            if not enrollments: return False, "Lớp chưa có sinh viên nào đăng ký!"
            
            count = 0
            for en in enrollments:
                new_hw = Assignment(class_id=class_id, student_id=en.student_id, status="Chưa nộp")
                db.add(new_hw)
                count += 1
            db.commit()
            return True, f"Đã phát bài tập thành công cho {count} sinh viên!"
        finally:
            db.close()

    def get_assignments(self) -> list:
        db = SessionLocal()
        try:
            data = db.query(Assignment, User).join(User, Assignment.student_id == User.user_id).all()
            return [{"uid": u.user_id, "name": u.name, "status": a.status, "time": a.submit_time or "---"} for a, u in data]
        finally:
            db.close()

    def send_assignment_reminders(self) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            unsubmitted = db.query(Assignment).filter(Assignment.status == "Chưa nộp").all()
            if not unsubmitted: return True, "Tuyệt vời! Tất cả sinh viên đã nộp bài."
            count = 0
            time_now = datetime.now().strftime("%d/%m/%Y %H:%M")
            for hw in unsubmitted:
                msg = f"⚠️ Nhắc nhở: Bạn chưa nộp bài tập lớp {hw.class_id}!"
                noti = Notification(user_id=hw.student_id, message=msg, created_at=time_now)
                db.add(noti)
                count += 1
            db.commit()
            return True, f"Đã gửi thông báo đến {count} sinh viên chưa nộp bài!"
        finally:
            db.close()

class AcademicStaffController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def execute_scholarship_filter(self, slots: int) -> list:
        if slots <= 0: return []
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff": return []
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student').all()
            eligible_list = [{"uid": s.user_id, "name": s.name, "score": (s.gpa * 0.8) + (s.rls * 0.2 / 4)} for s in students if s.credits >= 18 and s.rls > 80]
            return sorted(eligible_list, key=lambda x: x['score'], reverse=True)[:slots]
        finally:
            db.close()

    def load_pie_chart_data(self) -> dict:
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student').all()
            stats = {"Xuất sắc": 0, "Giỏi": 0, "Khá": 0, "Trung bình": 0}
            for s in students:
                if s.gpa >= 3.6: stats["Xuất sắc"] += 1
                elif s.gpa >= 3.2: stats["Giỏi"] += 1
                elif s.gpa >= 2.5: stats["Khá"] += 1
                else: stats["Trung bình"] += 1
            return stats
        finally:
            db.close()

    def get_at_risk_students(self)->list:
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student', (User.gpa < 2.8) | (User.attendance_rate < 0.8)).all()
            return [{"uid": s.user_id, "name": s.name, "gpa": s.gpa, "att": s.attendance_rate, "status": s.academic_status} for s in students]
        finally:
            db.close()

    def update_student_status(self, uid: str, new_status: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            student = db.query(User).filter(User.user_id == uid, User.role == 'Student').first()
            if not student: return False, "Không tìm thấy sinh viên."
            student.academic_status = new_status
            db.commit()
            return True, f"Đã chuyển trạng thái SV {student.name} thành: [{new_status}]"
        finally:
            db.close()

    def export_report_to_excel(self, file_path: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student').all()
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["Mã SV", "Họ Tên", "Email", "GPA", "ĐRL", "Tín chỉ", "Chuyên cần", "Trạng thái"])
                for s in students: writer.writerow([s.user_id, s.name, s.email, s.gpa, s.rls, s.credits, s.attendance_rate, s.academic_status])
            return True, "Xuất báo cáo Excel thành công!"
        finally:
            db.close()
    
    def get_all_users(self) -> list:
        db = SessionLocal()
        try:
            users = db.query(User).all()
            return [{"uid": u.user_id, "name": u.name, "email": u.email, "role": u.role} for u in users]
        finally:
            db.close()

    def create_user(self, uid, name, email, pwd, role) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            if db.query(User).filter((User.user_id == uid) | (User.email == email)).first():
                return False, "Lỗi: Mã ID hoặc Email đã tồn tại trong hệ thống!"
            new_user = User(user_id=uid, name=name, email=email, password=hash_pwd(pwd), role=role)
            db.add(new_user)
            db.commit()
            return True, f"Đã tạo tài khoản {role} thành công!"
        finally:
            db.close()

    def update_user(self, uid, name, email, pwd, role) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == uid).first()
            if not user: return False, "Lỗi: Không tìm thấy tài khoản!"
            
            duplicate = db.query(User).filter(User.email == email, User.user_id != uid).first()
            if duplicate: return False, "Lỗi: Email này đã được sử dụng cho tài khoản khác!"
            
            user.name, user.email, user.role = name, email, role
            if pwd != "******": user.password = hash_pwd(pwd)
            db.commit()
            return True, "Cập nhật thông tin thành công!"
        finally:
            db.close()

    def delete_user(self, uid) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == uid).first()
            if not user: return False, "Lỗi: Không tìm thấy tài khoản!"
            
            if user.role == 'Lecturer':
                if db.query(CourseClass).filter(CourseClass.lecturer_id == uid).first():
                    return False, "⛔ Không thể xóa Giảng viên đang có lớp! Hãy chuyển lớp trước."
            
            db.query(Enrollment).filter(Enrollment.student_id == uid).delete()
            db.query(Assignment).filter(Assignment.student_id == uid).delete()
            db.query(Notification).filter(Notification.user_id == uid).delete()
            db.query(CompletedCourse).filter(CompletedCourse.student_id == uid).delete()
            db.query(Project).filter((Project.student_id == uid) | (Project.lecturer_id == uid)).delete()
            
            db.delete(user)
            db.commit()
            return True, "Đã xóa tài khoản và dọn dẹp sạch sẽ CSDL."
        finally:
            db.close()