from models.models import SessionLocal, User, Course, CourseClass, Enrollment, Project, CompletedCourse, Assignment, Notification
import csv
from datetime import datetime

class MainController:
    def __init__(self):
        self.current_user = None

    def login(self, email: str, password: str) -> tuple[bool, str, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return False, "Email không tồn tại trên hệ thống.", ""
            
            if user.password != password:
                return False, "Mật khẩu không chính xác", ""
            
            self.current_user = user
            return True, f"Chào mừng {user.name} quay trở lại!", user.role
        except Exception as e:
            return False, f"Lỗi hệ thống: {str(e)}", ""
        finally:
            db.close()

    def logout(self):
        self.current_user = None


class StudentController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def get_dashboard_info(self) -> dict:
        if not self.main_ctrl.current_user:
            return {"profile": {"name": "N/A", "uid": "N/A"}, "warning": {"message": "Chưa đăng nhập"}, "classes": []}
        
        db = SessionLocal()
        try:
            student = db.query(User).filter(User.user_id == self.main_ctrl.current_user.user_id).first()
            
            is_warned = False
            warn_msg = "Trạng thái học tập bình thường."
            if student.gpa < 2.8 or student.attendance_rate < 0.8:
                is_warned = True
                warn_msg = f"Cảnh báo: Sinh viên {student.name} có GPA hoặc tỷ lệ chuyên cần dưới mức quy định!"

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
            
            if not course_class:
                return False, "Lớp học phần yêu cầu không tồn tại."

            course = db.query(Course).filter(Course.course_id == course_class.course_id).first()
            if course.prerequisite_id:
                completed = db.query(CompletedCourse).filter(
                    CompletedCourse.student_id == student_id,
                    CompletedCourse.course_id == course.prerequisite_id
                ).first()

                if not completed or completed.grade_letter == 'F':
                    suggestion = f" Bạn có thể học môn {course.alternative_course_id} để thay thế." if course.alternative_course_id else ""
                    return False, f"Bị chặn: Bạn chưa hoàn thành môn tiên quyết {course.prerequisite_id}!{suggestion}"

            exist_en = db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first()
            if exist_en:
                return False, "Bạn đã đăng ký lớp học phần này rồi."

            new_en = Enrollment(class_id=class_id, student_id=student_id)
            db.add(new_en)
            db.commit()
            return True, f"Đăng ký thành công lớp {class_id}."
        except Exception as e:
            db.rollback()
            return False, f"Lỗi tác vụ: {str(e)}"
        finally:
            db.close()

    def check_in_attendance(self, class_id: str, code: str) -> tuple[bool, str]:
        if not self.main_ctrl.current_user: return False, "Lỗi: Chưa đăng nhập."
        db = SessionLocal()
        try:
            student_id = self.main_ctrl.current_user.user_id
            course_class = db.query(CourseClass).filter(CourseClass.class_id == class_id).first()
            
            if not course_class:
                return False, "Không tìm thấy lớp học phần."
            if not course_class.attendance_code or course_class.attendance_code != code:
                return False, "Mã điểm danh không hợp lệ hoặc phiên điểm danh đã đóng."

            enrollment = db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first()
            if not enrollment:
                return False, "Bạn không có tên trong lớp học phần này."

            enrollment.chuyen_can = min(10.0, enrollment.chuyen_can + 1.0)
            db.commit()
            return True, "Xác nhận điểm danh thành công! Điểm chuyên cần đã được cập nhật."
        except Exception as e:
            db.rollback()
            return False, f"Điểm danh thất bại: {str(e)}"
        finally:
            db.close()

    def get_notifications(self) -> list:
        if not self.main_ctrl.current_user: return []
        db = SessionLocal()
        try:
            notis = db.query(Notification).filter(Notification.user_id == self.main_ctrl.current_user.user_id).all()
            return [{"msg": n.message, "time": n.created_at} for n in notis]
        finally:
            db.close()

    def get_assignments(self) -> list:
        if not self.main_ctrl.current_user: return []
        db = SessionLocal()
        try:
            hws = db.query(Assignment).filter(Assignment.student_id == self.main_ctrl.current_user.user_id).all()
            return [{"id": a.id, "class_id": a.class_id, "status": a.status, "time": a.submit_time} for a in hws]
        finally:
            db.close()

    def submit_assignment(self, assignment_id: int) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            hw = db.query(Assignment).filter(Assignment.id == assignment_id).first()
            if not hw: return False, "Không tìm thấy bài tập."
            if hw.status == "Đã nộp": return False, "Bạn đã nộp bài này rồi!"
            
            hw.status = "Đã nộp"
            hw.submit_time = datetime.now().strftime("%d/%m/%Y %H:%M")
            db.commit()
            return True, "Nộp bài thành công!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi nộp bài: {str(e)}"
        finally:
            db.close()

    def get_detailed_grades(self) -> list:
        if not self.main_ctrl.current_user: return []
        db = SessionLocal()
        try:
            enrollments = db.query(Enrollment).filter(Enrollment.student_id == self.main_ctrl.current_user.user_id).all()
            return [{
                "class_id": e.class_id, "cc": e.chuyen_can, "gk": e.giua_ky, 
                "ck": e.cuoi_ky, "tong": e.diem_tong_ket, "he4": e.diem_he_4
            } for e in enrollments]
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
        if not self.main_ctrl.current_user: return False, "Lỗi: Chưa đăng nhập."
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(
                CourseClass.class_id == class_id, 
                CourseClass.lecturer_id == self.main_ctrl.current_user.user_id
            ).first()
            
            if not course_class:
                return False, "Bạn không có quyền hoặc lớp không tồn tại."
            
            course_class.attendance_code = token_code
            db.commit()
            return True, f"Mở phiên điểm danh lớp {class_id} với mã: {token_code}"
        finally:
            db.close()

    def input_grade(self, class_id: str, student_id: str, score_type: str, value: float) -> tuple[bool, str]:
        if not self.main_ctrl.current_user: return False, "Lỗi: Chưa đăng nhập."
        db = SessionLocal()
        try:
            course_class = db.query(CourseClass).filter(
                CourseClass.class_id == class_id,
                CourseClass.lecturer_id == self.main_ctrl.current_user.user_id
            ).first()
            if not course_class:
                return False, "Bạn không phụ trách lớp học phần này."

            enrollment = db.query(Enrollment).filter_by(class_id=class_id, student_id=student_id).first()
            if not enrollment:
                return False, "Sinh viên không nằm trong danh sách lớp."
            if enrollment.is_locked:
                return False, "Bảng điểm đã bị khóa, không thể chỉnh sửa."

            if score_type == 'chuyen_can': enrollment.chuyen_can = value
            elif score_type == 'giua_ky': enrollment.giua_ky = value
            elif score_type == 'cuoi_ky': enrollment.cuoi_ky = value
            else: return False, "Loại điểm số không hợp lệ."
            
            db.commit()
            return True, f"Đã cập nhật điểm {score_type} cho sinh viên UID:{student_id}."
        except Exception as e:
            db.rollback()
            return False, f"Lỗi cập nhật điểm: {str(e)}"
        finally:
            db.close()
        
    def calculate_final_grades(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()
            if not enrollments: return False, "Lớp không tồn tại hoặc chưa có sinh viên."
            
            for e in enrollments:
                cc = e.chuyen_can or 0.0
                gk = e.giua_ky or 0.0
                ck = e.cuoi_ky or 0.0
                tong = (cc * 0.1) + (gk * 0.2) + (ck * 0.7)
                e.diem_tong_ket = round(tong, 2)
                
                if tong >= 8.5: e.diem_he_4 = 4.0
                elif tong >= 7.0: e.diem_he_4 = 3.0
                elif tong >= 5.5: e.diem_he_4 = 2.0
                elif tong >= 4.0: e.diem_he_4 = 1.0
                else: e.diem_he_4 = 0.0
            
            db.commit()
            return True, f"Đã tính xong điểm tổng kết cho {len(enrollments)} sinh viên lớp {class_id}."
        except Exception as e:
            db.rollback()
            return False, f"Lỗi tính điểm: {str(e)}"
        finally:
            db.close()

    def lock_class_grades(self, class_id: str) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            enrollments = db.query(Enrollment).filter(Enrollment.class_id == class_id).all()
            if not enrollments: return False, "Lớp không có dữ liệu."
            for e in enrollments:
                e.is_locked = True
            db.commit()
            return True, f"🔒 Đã khóa sổ điểm lớp {class_id}. Không ai được sửa nữa!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi khóa điểm: {str(e)}"
        finally:
            db.close()

    def get_assignments(self) -> list:
        db = SessionLocal()
        try:
            data = db.query(Assignment, User).join(User, Assignment.student_id == User.user_id).all()
            return [{"uid": u.user_id, "name": u.name, "status": a.status, "time": a.submit_time or "---"} for a, u in data]
        except Exception as e:
            print(f"Lỗi lấy bài tập: {e}")
            return []
        finally:
            db.close()

    def send_assignment_reminders(self) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            unsubmitted = db.query(Assignment).filter(Assignment.status == "Chưa nộp").all()
            if not unsubmitted:
                return True, "Tuyệt vời! Tất cả sinh viên đã nộp bài."
            
            count = 0
            time_now = datetime.now().strftime("%d/%m/%Y %H:%M")
            for hw in unsubmitted:
                msg = f"⚠️ Nhắc nhở quá hạn: Bạn chưa nộp bài tập lớp {hw.class_id}!"
                noti = Notification(user_id=hw.student_id, message=msg, created_at=time_now)
                db.add(noti)
                count += 1
            
            db.commit()
            return True, f"Đã tự động gửi thông báo đến {count} sinh viên chưa nộp bài!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi gửi nhắc nhở: {str(e)}"
        finally:
            db.close()


class AcademicStaffController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def execute_scholarship_filter(self, slots: int) -> list:
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff": 
            print("🛑 Lỗi Bảo Mật: Bạn không có quyền truy cập chức năng của Giáo vụ!")
            return []
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student').all()
            eligible_list = []

            for s in students:
                if s.credits >= 18 and s.rls > 80:
                    score = (s.gpa * 0.8) + (s.rls * 0.2 / 4)
                    eligible_list.append({"uid": s.user_id, "name": s.name, "score": score})
            
            sorted_winners = sorted(eligible_list, key=lambda x: x['score'], reverse=True)
            return sorted_winners[:slots]
        finally:
            db.close()

    def load_pie_chart_data(self) -> dict:
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff":
            print("🛑 Lỗi Bảo Mật: Bạn không có quyền xem thống kê toàn khóa!")
            return {}
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
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff":
            return []
        db = SessionLocal()
        try:
            students = db.query(User).filter(
                User.role == 'Student',
                (User.gpa < 2.8) | (User.attendance_rate < 0.8)
            ).all()
            return [{"uid": s.user_id, "name": s.name, "gpa": s.gpa, "att": s.attendance_rate, "status": s.academic_status} for s in students]
        finally:
            db.close()

    def update_student_status(self, uid: str, new_status: str) -> tuple[bool, str]:
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff":
            return False, "Lỗi bảo mật: Không đủ quyền hạn."
        db = SessionLocal()
        try:
            student = db.query(User).filter(User.user_id == uid, User.role == 'Student').first()
            if not student:
                return False, "Không tìm thấy sinh viên."
            
            student.academic_status = new_status
            db.commit()
            return True, f"Đã chuyển trạng thái SV {student.name} thành: [{new_status}]"
        except Exception as e:
            db.rollback()
            return False, str(e)
        finally:
            db.close()

    def export_report_to_excel(self, file_path: str) -> tuple[bool, str]:
        if not self.main_ctrl.current_user or self.main_ctrl.current_user.role != "Staff":
            return False, "Lỗi bảo mật."
        db = SessionLocal()
        try:
            students = db.query(User).filter(User.role == 'Student').all()
            with open(file_path, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(["Mã SV", "Họ Tên", "Email", "GPA", "ĐRL", "Tín chỉ", "Chuyên cần", "Trạng thái"])
                for s in students:
                    writer.writerow([s.user_id, s.name, s.email, s.gpa, s.rls, s.credits, s.attendance_rate, s.academic_status])
            return True, "Xuất báo cáo Excel thành công!"
        except Exception as e:
            return False, f"Lỗi xuất file: {e}"
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
            new_user = User(user_id=uid, name=name, email=email, password=pwd, role=role)
            db.add(new_user)
            db.commit()
            return True, f"Đã tạo tài khoản {role} thành công!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi CSDL: {str(e)}"
        finally:
            db.close()

    def update_user(self, uid, name, email, pwd, role) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == uid).first()
            if not user: return False, "Lỗi: Không tìm thấy tài khoản!"
            user.name, user.email, user.password, user.role = name, email, pwd, role
            db.commit()
            return True, "Cập nhật thông tin thành công!"
        except Exception as e:
            db.rollback()
            return False, f"Lỗi CSDL: {str(e)}"
        finally:
            db.close()

    def delete_user(self, uid) -> tuple[bool, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.user_id == uid).first()
            if not user: return False, "Lỗi: Không tìm thấy tài khoản!"
            db.delete(user)
            db.commit()
            return True, "Đã xóa tài khoản vĩnh viễn khỏi hệ thống."
        except Exception as e:
            db.rollback()
            return False, f"Lỗi (Có thể do dính khóa ngoại): {str(e)}"
        finally:
            db.close()