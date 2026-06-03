# BCSE Management System - Hệ thống quản lí học vụ 

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Matplotlib](https://img.shields.io/badge/Data_Viz-Matplotlib-blueviolet.svg)

## 📖 1. Mô tả dự án 
*BCSE Management System* là một phần mềm Desktop Application được phát triển bằng Python bởi team *3RR0R*, mô phỏng hệ thống quản lý đào tạo tín chỉ khép kín của ngành KH-KT máy tính ĐHVN, ĐHQGHN. 

Dự án được xây dựng dựa trên kiến trúc *MVC (Model - View - Controller)* kết hợp *ORM (Object-Relational Mapping)*, mang đến một hệ sinh thái đồng bộ dữ liệu theo thời gian thực giữa 3 phân hệ người dùng: Giáo vụ (Staff), Giảng viên (Lecturer), và Sinh viên (Student). 

Điểm nhấn của hệ thống là giao diện người dùng (UI/UX) được thiết kế theo ngôn ngữ *HyperOS* , mang lại trải nghiệm phần mềm thương mại hiện đại, vượt xa các đồ án giao diện Tkinter truyền thống.

---

## 2. Tính năng nổi bật

### Bảo mật & Phân quyền 
- *Password Hashing:* Thuật toán băm PBKDF2-HMAC-SHA256 (100.000 vòng lặp) kết hợp *Dynamic Salting* (dùng Email làm Salt), chống tấn công Brute-force & Rainbow Tables.
- *RBAC :* Phân quyền hiển thị UI và chặn thực thi API ở tầng Controller theo 3 Role riêng biệt.

### Phân hệ giáo vụ (Admin / Staff)
- *Quản lý hệ thống (CRUD):* Quản lý Tài khoản, Môn học, và Mở Lớp học phần với các ràng buộc chặt chẽ (Môn tiên quyết, Giới hạn sĩ số).
- *Cảnh báo học vụ sớm:* Tự động quét sinh viên có điểm GPA < 2.8 hoặc chuyên cần < 80% để cảnh cáo/đình chỉ học(cấm thi).
- *Xét học bổng tự động:* Thuật toán lọc sinh viên đủ tín chỉ, tính RankScore (80% GPA + 20% ĐRL) và xếp hạng.
- *Thống kê trực quan:* Trích xuất dữ liệu CSDL sang biểu đồ tròn 3D  tự động đổi màu theo Theme, và xuất báo cáo CSV/Excel.

### Phân hệ giảng viên (Lecturer)
- *Quản lý điểm :* Nhập điểm thành phần, tự động tính tổng Hệ 10, quy đổi Hệ 4, Điểm chữ (A-F). Tính năng "Khóa sổ" tự động cập nhật GPA và Tín chỉ tích lũy (Loại bỏ điểm F).
- *Điểm danh thông minh:* Kích hoạt phiên điểm danh bằng mã *OTP ngẫu nhiên*.
- *Quản lý bài tập:* Phát bài tập cho lớp và gửi thông báo nhắc nhở đồng loạt tới hòm thư sinh viên.

### Phân hệ Sinh viên (Student)
- *Dashboard Tổng quan:* Theo dõi GPA, Tín chỉ tích lũy, trạng thái cảnh báo và hòm thư nhắc nhở theo thời gian thực.
- *Đăng ký học phần :* Hệ thống chặn tự động nếu: Trùng lặp, Lớp đã đầy sĩ số, Chưa qua môn tiên quyết, hoặc đã học qua môn này.
- *Điểm danh & Nộp bài:* Nhập mã OTP từ giảng viên để tự động cộng điểm chuyên cần.

---

## 3. Công nghệ sử dụng

* *Ngôn ngữ:* Python 3.x
* *Kiến trúc:* MVC (Model - View - Controller)
* *Giao diện (GUI):* CustomTkinter (Modern UI), tkinter
* *Cơ sở dữ liệu:* SQLite3
* *ORM:* SQLAlchemy (Bảo vệ chống SQL Injection & Race Condition)
* *Xử lý số liệu & Biểu đồ:* matplotlib
* *Bảo mật:* hashlib, binascii

---

## 4. Hướng dẫn cài đặt & Khởi chạy 

Vui lòng mở Terminal (hoặc Command Prompt) và chạy lần lượt các lệnh sau:

```bash
# Bước 1: Clone dự án và di chuyển vào thư mục
git clone https://github.com/WataruAki/Team_3RR0R_OOP.git
cd Team_3RR0R_OOP

# Bước 2: Cài đặt các thư viện phụ thuộc
pip install -r requirements.txt

# Bước 3: Khởi tạo Cơ sở dữ liệu & Dữ liệu mẫu (Seed Data)
python main.py

# Bước 4: Chạy Ứng dụng chính
python ViewBCSE.py

## 5. Tài khoản mẫu 
Sau khi chạy lệnh python main.py thành công, bạn có thể đăng nhập bằng các tài khoản dưới đây ( Mật khẩu chung cho tất cả là: **12345678**):

| Vai trò (Role) | Email Đăng nhập | Ghi chú |
| :--- | :--- | :--- |
| *Giáo vụ* | giaovu@vnu.edu.vn | Toàn quyền Admin hệ thống |
| *Giảng viên* | giangvien@vnu.edu.vn | Phụ trách lớp CSE3011_C1, WEB2011_C1 |
| *Sinh viên (Tốt)* | anhhv@vnu.edu.vn | Sinh viên Hoàng Việt Anh (GPA cao) |
| **Sinh viên (Kém)**| cabiet@vnu.edu.vn | Test tính năng Cảnh báo học vụ |

---
Developed by Team 3RR0R.

Hà Nội, tháng 5-6 năm 2026