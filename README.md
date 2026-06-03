# 🎓 BCSE Management System - Hệ thống Quản lý Học vụ Toàn diện

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-brightgreen.svg)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📖 1. Mô tả dự án (Project Description)
**BCSE Management System** là một phần mềm Desktop Application được phát triển bằng Python bởi team **3RR0R**, mô phỏng hệ thống quản lý đào tạo tín chỉ khép kín của Trường Đại học. 

Dự án được xây dựng dựa trên kiến trúc **MVC (Model - View - Controller)** kết hợp **ORM (Object-Relational Mapping)**, mang đến một hệ sinh thái đồng bộ dữ liệu theo thời gian thực (Real-time) giữa 3 phân hệ người dùng: Giáo vụ (Staff), Giảng viên (Lecturer), và Sinh viên (Student). 

Điểm nhấn của hệ thống là giao diện người dùng (UI/UX) được thiết kế theo ngôn ngữ **HyperOS** (Bo góc Squircles sâu, Dark/Light Mode tự động, đổ bóng 3D), mang lại trải nghiệm phần mềm thương mại hiện đại, vượt xa các đồ án giao diện Tkinter truyền thống.

---

## ✨ 2. Tính năng nổi bật (Key Features)

### 🛡️ Bảo mật & Phân quyền (Security & RBAC)
- **Password Hashing:** Thuật toán băm `PBKDF2-HMAC-SHA256` (100.000 vòng lặp) kết hợp **Dynamic Salting** (dùng Email làm Salt), chống tấn công Brute-force & Rainbow Tables.
- **RBAC (Role-Based Access Control):** Phân quyền hiển thị UI và chặn thực thi API ở tầng Controller theo 3 Role riêng biệt.

### 🏢 Phân hệ Giáo vụ (Admin / Staff)
- **Quản lý Hệ thống (CRUD):** Quản lý Tài khoản, Môn học, và Mở Lớp học phần với các ràng buộc chặt chẽ (Môn tiên quyết, Giới hạn sĩ số).
- **Cảnh báo Học vụ sớm:** Tự động quét sinh viên có điểm `GPA < 2.8` hoặc `Chuyên cần < 80%` để cảnh cáo/đình chỉ.
- **Xét duyệt Học bổng tự động:** Thuật toán lọc sinh viên đủ tín chỉ, tính `RankScore` (80% GPA + 20% ĐRL) và xếp hạng.
- **Thống kê Trực quan:** Trích xuất dữ liệu CSDL sang biểu đồ tròn 3D (Matplotlib) tự động đổi màu theo Theme, và xuất báo cáo CSV/Excel.

### 👨‍🏫 Phân hệ Giảng viên (Lecturer)
- **Quản lý Điểm (Incremental Update):** Nhập điểm thành phần, tự động tính tổng Hệ 10, quy đổi Hệ 4, Điểm chữ (A-F). Tính năng "Khóa sổ" tự động cập nhật GPA và Tín chỉ tích lũy (Loại bỏ điểm F).
- **Điểm danh thông minh:** Kích hoạt phiên điểm danh bằng mã **OTP ngẫu nhiên**.
- **Quản lý Bài tập:** Phát bài tập cho lớp và gửi "Notification" nhắc nhở đồng loạt tới hòm thư sinh viên.

### 👨‍🎓 Phân hệ Sinh viên (Student)
- **Dashboard Tổng quan:** Theo dõi GPA, Tín chỉ tích lũy, trạng thái cảnh báo và hòm thư nhắc nhở theo thời gian thực.
- **Đăng ký Học phần (Constraint-based):** Hệ thống chặn tự động nếu: Trùng lặp, Lớp đã đầy sĩ số, Chưa qua môn tiên quyết, hoặc Đã học qua môn này.
- **Điểm danh & Nộp bài:** Nhập mã OTP từ giảng viên để tự động cộng điểm chuyên cần.

---

## 🛠️ 3. Công nghệ sử dụng (Tech Stack)

* **Ngôn ngữ:** `Python 3.x`
* **Kiến trúc:** `MVC` (Model - View - Controller)
* **Giao diện (GUI):** `customtkinter` (Modern UI), `tkinter`
* **Cơ sở dữ liệu:** `SQLite3`
* **ORM:** `SQLAlchemy` (Bảo vệ chống SQL Injection & Race Condition)
* **Xử lý số liệu & Biểu đồ:** `matplotlib`
* **Bảo mật:** `hashlib`, `binascii`

---

## 🚀 4. Hướng dẫn Cài đặt & Khởi chạy (Installation & Setup)

**Bước 1: Clone dự án và di chuyển vào thư mục**
```bash
git clone [https://github.com/your-username/Team_3RR0R_OOP.git](https://github.com/your-username/Team_3RR0R_OOP.git)
cd Team_3RR0R_OOP
**Bước 2: Cài đặt các thư viện phụ thuộc**
```bash
pip install -r requirements.txt
**Bước 3: Khởi tạo Cơ sở dữ liệu & Dữ liệu mẫu (Seed Data)**
```bash
python main.py
**Bước 4: Chạy Ứng dụng**
```bash
python ViewBCSE.py
<img width="871" height="390" alt="image" src="https://github.com/user-attachments/assets/07be0d2a-cb41-4508-b8f7-b54804017642" />
Developed with ❤️ by Team 3RR0R.
