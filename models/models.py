from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    gpa = Column(Float, server_default=text('0.0'))
    rls = Column(Integer, server_default=text('0'))
    credits = Column(Integer, server_default=text('0'))
    attendance_rate = Column(Float, server_default=text('1.0'))
    academic_status = Column(String, server_default=text("'Bình thường'"))

    # VÁ LỖ HỔNG DATABASE INTEGRITY: Cấu hình Xóa dây chuyền tự động (Cascade Delete)
    enrollments = relationship("Enrollment", back_populates="student", cascade="all, delete-orphan")
    completed_courses = relationship("CompletedCourse", back_populates="student", cascade="all, delete-orphan")

class Course(Base):
    __tablename__ = 'courses'
    course_id = Column(String, primary_key=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    prerequisite_id = Column(String, ForeignKey('courses.course_id'), nullable=True)
    alternative_course_id = Column(String, ForeignKey('courses.course_id'), nullable=True)

    prerequisite = relationship("Course", remote_side=[course_id], foreign_keys=[prerequisite_id])
    alternative_course = relationship("Course", remote_side=[course_id], foreign_keys=[alternative_course_id])

class CourseClass(Base):
    __tablename__ = 'course_classes'
    class_id = Column(String, primary_key=True)
    course_id = Column(String, ForeignKey('courses.course_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    attendance_code = Column(String, nullable=True)
    max_capacity = Column(Integer, server_default=text('40'))

    course = relationship("Course")
    lecturer = relationship("User")

class Enrollment(Base):
    __tablename__ = 'enrollments'
    class_id = Column(String, ForeignKey('course_classes.class_id'), primary_key=True)
    student_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    chuyen_can = Column(Float, server_default=text('0.0'))
    giua_ky = Column(Float, server_default=text('0.0'))
    cuoi_ky = Column(Float, server_default=text('0.0'))
    
    diem_tong_ket = Column(Float, nullable=True) 
    diem_he_4 = Column(Float, nullable=True)     
    is_locked = Column(Boolean, server_default=text('0'))
    
    # VÁ LỖ HỔNG 1: Chống Spam Điểm danh
    last_otp = Column(String, nullable=True)

    course_class = relationship("CourseClass")
    student = relationship("User", back_populates="enrollments")

class Project(Base):
    __tablename__ = 'projects'
    project_id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    status = Column(String, server_default=text("'Đang thực hiện'"))

    student = relationship("User", foreign_keys=[student_id])
    lecturer = relationship("User", foreign_keys=[lecturer_id])

class CompletedCourse(Base):
    __tablename__ = 'completed_courses'
    student_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    course_id = Column(String, ForeignKey('courses.course_id'), primary_key=True)
    grade_letter = Column(String, nullable=False)

    student = relationship("User", back_populates="completed_courses")
    course = relationship("Course")

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True, autoincrement=True)
    class_id = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('users.user_id'))
    status = Column(String, server_default=text("'Chưa nộp'")) 
    submit_time = Column(String, nullable=True)
    student = relationship("User")

class Notification(Base):
    __tablename__ = 'notifications'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    message = Column(String, nullable=False)
    is_read = Column(Boolean, server_default=text('0'))
    created_at = Column(String, nullable=True)
    user = relationship("User")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
db_path = os.path.join(ROOT_DIR, 'hms_database.db')
DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    Base.metadata.create_all(bind=engine)
    print("Đã khởi tạo CSDL: hms_database.db an toàn.")

if __name__ == "__main__":
    create_database()