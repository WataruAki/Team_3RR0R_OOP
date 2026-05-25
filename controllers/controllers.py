from models.models import SessionLocal, User, Course, CourseClass, Enrollment, Project, CompletedCourse

class MainController:
    def __init__(self):
        self.current_user = None

    def login(self, email: str) -> tuple[bool, str, str]:
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                return False, "Email không tồn tại trên hệ thống.", ""
            
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


class AcademicStaffController:
    def __init__(self, main_controller: MainController):
        self.main_ctrl = main_controller

    def execute_scholarship_filter(self, slots: int) -> list:
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