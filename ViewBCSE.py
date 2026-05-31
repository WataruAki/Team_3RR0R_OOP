from tkinter import *
from controllers import MainController

window = Tk()
window.title("BCSE - Dang Nhap")


frame = Frame(window, bd=1, relief="solid", bg="white", padx=30, pady=40)
frame.pack()
frame.grid_columnconfigure(0, weight=1)


label_mail = Label(frame,text="Gmail",font=("Segoe UI",10,"bold"))
enter_mail = Entry(frame,font=("Segoe UI",15),width="25")
label_mail.grid(row=0, column=0, sticky="w", pady=(0,4))
enter_mail.grid(row=1, column=0, sticky="ew", pady=(0,15))

label_password = Label(frame,text="Password",font=("Segoe UI",10,"bold"))
enter_password= Entry(frame,font=("Segoe UI",15),width="25",show="*")
label_password.grid(row=3, column=0, sticky="w", pady=(0,4))
enter_password.grid(row=4, column=0, sticky="ew", pady=(0,15))

def click():
    mail=enter_mail.get()
    password=enter_password.get()
    controller = MainController() # controller o day ne
    success, message, role = controller.login(mail,password)
    if success:
        if role == "Student":
            from student_view import StudentWindow
            print(message)
            StudentWindow(controller)
        elif role == "teacher":
            from teacher_view import LecturerWindow
            print(message)

            LecturerWindow()
        elif role =="giaovu":
            from acs_view import ASWindow
            print(message)
            ASWindow()
        window.destroy()
    else:
        label_error.config(text=message)
label_error = Label(frame, text="", fg="red", bg="white")
label_error.grid(row=6, column=0)

signin_btn = Button(frame,text ="Sign in",command = click)
signin_btn.grid(row=5, column =0, sticky="ew", pady=(10,0))
window.bind("<Return>", lambda event: click())

window.update()
w = window.winfo_width()
h = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (w // 2)
y = (window.winfo_screenheight() // 2) - (h // 2)
window.geometry(f"+{x}+{y}")

window.mainloop()