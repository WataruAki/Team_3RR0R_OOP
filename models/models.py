from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    # Đã sửa từ uid (INTEGER) thành user_id (String) để đồng bộ với các bảng khác
    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    gpa = Column(Float, server_default=text('0.0'))
    rls = Column(Integer, server_default=text('0'))
    credits = Column(Integer, server_default=text('0'))
    attendance_rate = Column(Float, server_default=text('1.0'))

    # Relationships (Tùy chọn nhưng nên có để truy vấn ORM thuận tiện)
    enrollments = relationship("Enrollment", back_populates="student")
    completed_courses = relationship("CompletedCourse", back_populates="student")


class Course(Base):
    __tablename__ = 'courses'

    course_id = Column(String, primary_key=True)
    course_name = Column(String, nullable=False)
    credits = Column(Integer, nullable=False)
    prerequisite_id = Column(String, ForeignKey('courses.course_id'), nullable=True)
    alternative_course_id = Column(String, ForeignKey('courses.course_id'), nullable=True)

    # Relationships cho cấu trúc tự tham chiếu (Self-referential)
    prerequisite = relationship("Course", remote_side=[course_id], foreign_keys=[prerequisite_id])
    alternative_course = relationship("Course", remote_side=[course_id], foreign_keys=[alternative_course_id])


class CourseClass(Base):
    __tablename__ = 'course_classes'

    class_id = Column(String, primary_key=True)
    course_id = Column(String, ForeignKey('courses.course_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    attendance_code = Column(String, nullable=True)

    # Relationships
    course = relationship("Course")
    lecturer = relationship("User")


class Enrollment(Base):
    __tablename__ = 'enrollments'

    class_id = Column(String, ForeignKey('course_classes.class_id'), primary_key=True)
    student_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    chuyen_can = Column(Float, server_default=text('0.0'))
    giua_ky = Column(Float, server_default=text('0.0'))
    cuoi_ky = Column(Float, server_default=text('0.0'))

    # Relationships
    course_class = relationship("CourseClass")
    student = relationship("User", back_populates="enrollments")


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(String, primary_key=True)
    project_name = Column(String, nullable=False)
    student_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    lecturer_id = Column(String, ForeignKey('users.user_id'), nullable=False)
    status = Column(String, server_default=text("'Đang thực hiện'"))

    # Relationships
    student = relationship("User", foreign_keys=[student_id])
    lecturer = relationship("User", foreign_keys=[lecturer_id])


class CompletedCourse(Base):
    __tablename__ = 'completed_courses'

    student_id = Column(String, ForeignKey('users.user_id'), primary_key=True)
    course_id = Column(String, ForeignKey('courses.course_id'), primary_key=True)
    grade_letter = Column(String, nullable=False)

    # Relationships
    student = relationship("User", back_populates="completed_courses")
    course = relationship("Course")


DATABASE_URL = "sqlite:///hms_database.db"
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_database():
    """Hàm tạo file hms_database.db và cấu trúc các bảng"""
    Base.metadata.create_all(bind=engine)
    print("Đã khởi tạo thành công CSDL: hms_database.db bằng SQLAlchemy")

if __name__ == "__main__":
    create_database()