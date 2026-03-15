import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from database import connect_db


def login_screen(root):

    conn, cursor = connect_db()

    for w in root.winfo_children():
        w.destroy()

    root.geometry("1000x650")
    root.configure(bg="#F3E8FF")

    # ---------- LEFT PANEL ----------
    left = tk.Frame(root, bg="#D81B60", width=380)
    left.pack(side="left", fill="y")

    tk.Label(left, text="AI HOSTEL\nMANAGEMENT",
             font=("Arial", 24, "bold"),
             fg="white", bg="#D81B60").place(x=40, y=220)

    tk.Label(left, text="Smart Room Allocation\nusing AI Optimization",
             font=("Arial", 12),
             fg="white", bg="#D81B60").place(x=40, y=320)

    # ---------- CARD ----------
    card = tk.Frame(root, bg="#FFE4F1", padx=50, pady=40)
    card.place(relx=0.68, rely=0.5, anchor="center")

    role_var = tk.StringVar(value="Student")

    # ---------- MESSAGE ----------
    def show_msg(text, color="#4CAF50"):

        msg = tk.Label(root, text=text,
                       bg=color, fg="white",
                       font=("Arial", 11, "bold"),
                       padx=20, pady=8)

        msg.place(relx=0.5, rely=0.05, anchor="center")

        root.after(2000, msg.destroy)

    # ---------- NEXT PAGE ----------
    def open_next_page(username):

        if role_var.get() == "Student":
            from student_panel import open_student
            open_student(root, username)
        else:
            from warden_panel import open_warden
            open_warden(root, username)

    # ---------- LOGIN ----------
    def show_login():

        for w in card.winfo_children():
            w.destroy()

        tk.Label(card, text="Login",
                 font=("Arial", 20, "bold"),
                 bg="#FFE4F1").pack(pady=10)

        tk.Label(card, text="User ID", bg="#FFE4F1").pack(anchor="w")
        userid_entry = tk.Entry(card, width=30, font=("Arial", 12))
        userid_entry.pack(pady=6, ipady=6)

        tk.Label(card, text="Password", bg="#FFE4F1").pack(anchor="w")
        password_entry = tk.Entry(card, show="*", width=30, font=("Arial", 12))
        password_entry.pack(pady=6, ipady=6)

        tk.Label(card, text="Role", bg="#FFE4F1").pack(anchor="w", pady=5)

        role_frame = tk.Frame(card, bg="#FFE4F1")
        role_frame.pack()

        tk.Radiobutton(role_frame, text="Student",
                       variable=role_var, value="Student",
                       bg="#FFE4F1").pack(side="left", padx=15)

        tk.Radiobutton(role_frame, text="Warden",
                       variable=role_var, value="Warden",
                       bg="#FFE4F1").pack(side="left", padx=15)

        # ---------- LOGIN FUNCTION ----------
        def login():

            uid = userid_entry.get()
            pwd = password_entry.get()

            if uid == "" or pwd == "":
                show_msg("Fill all fields", "#E53935")
                return

            if role_var.get() == "Student":
                cursor.execute(
                    "SELECT username FROM users WHERE roll_no=? AND password=?",
                    (uid, pwd))
            else:
                cursor.execute(
                    "SELECT username FROM users WHERE userid=? AND password=?",
                    (uid, pwd))

            res = cursor.fetchone()

            if res:
                show_msg("Login Successful")
                root.after(2000, lambda: open_next_page(res[0]))
            else:
                show_msg("Invalid ID or Password", "#E53935")

        # ---------- FORGOT PASSWORD ----------
        def forgot_password():

            uid = userid_entry.get()

            if uid == "":
                show_msg("Enter User ID first", "#E53935")
                return

            phone = simpledialog.askstring(
                "Verify", "Enter your registered phone:")

            if not phone:
                return

            if role_var.get() == "Student":
                cursor.execute(
                    "SELECT username FROM users WHERE roll_no=? AND phone=?",
                    (uid, phone))
            else:
                cursor.execute(
                    "SELECT username FROM users WHERE userid=? AND phone=?",
                    (uid, phone))

            res = cursor.fetchone()

            if res:

                new_pass = simpledialog.askstring(
                    "Reset Password",
                    "Enter new password:",
                    show="*")

                if new_pass:

                    if role_var.get() == "Student":
                        cursor.execute(
                            "UPDATE users SET password=? WHERE roll_no=?",
                            (new_pass, uid))
                    else:
                        cursor.execute(
                            "UPDATE users SET password=? WHERE userid=?",
                            (new_pass, uid))

                    conn.commit()

                    show_msg("Password Reset Successful")

            else:
                show_msg("User not found", "#E53935")

        # ---------- BUTTONS ----------
        tk.Button(card, text="LOGIN",
                  command=login,
                  bg="#BA68C8",
                  fg="white",
                  width=22,
                  font=("Arial", 12, "bold")).pack(pady=12, ipady=6)

        tk.Button(card, text="SIGN UP",
                  command=show_signup,
                  bg="#D81B60",
                  fg="white",
                  width=22,
                  font=("Arial", 12, "bold")).pack(ipady=6, pady=5)

        tk.Button(card, text="Forgot Password",
                  command=forgot_password,
                  bg="#FF7043",
                  fg="white",
                  width=22,
                  font=("Arial", 11, "bold")).pack(pady=5)

    # ---------- SIGNUP ----------
    def show_signup():

        for w in card.winfo_children():
            w.destroy()

        tk.Label(card, text="Sign Up",
                 font=("Arial", 20, "bold"),
                 bg="#FFE4F1").pack(pady=10)

        tk.Label(card, text="Username", bg="#FFE4F1").pack(anchor="w")
        username_entry = tk.Entry(card, width=30, font=("Arial", 12))
        username_entry.pack(pady=5, ipady=6)

        dep_label = tk.Label(card, text="Department", bg="#FFE4F1")
        dep_entry = tk.Entry(card, width=30, font=("Arial", 12))
        dep_label.pack(anchor="w")
        dep_entry.pack(pady=5, ipady=6)
        
        tk.Label(card, text="Year", bg="#FFE4F1").pack(anchor="w")
        year_var = tk.StringVar()
        ttk.Combobox( card, textvariable=year_var, values=["1","2","3","4"], width=28,
                     font=("Arial",12)).pack(pady=5, ipady=4)
        
        id_label = tk.Label(card, text="Roll No", bg="#FFE4F1")
        id_entry = tk.Entry(card, width=30, font=("Arial", 12))
        id_label.pack(anchor="w")
        id_entry.pack(pady=5, ipady=6)

        tk.Label(card, text="Phone", bg="#FFE4F1").pack(anchor="w")
        phone_entry = tk.Entry(card, width=30, font=("Arial", 12))
        phone_entry.pack(pady=5, ipady=6)

        tk.Label(card, text="Password", bg="#FFE4F1").pack(anchor="w")
        password_entry = tk.Entry(card, show="*", width=30, font=("Arial", 12))
        password_entry.pack(pady=5, ipady=6)

        tk.Label(card, text="Role", bg="#FFE4F1").pack(anchor="w", pady=5)

        role_frame = tk.Frame(card, bg="#FFE4F1")
        role_frame.pack()

        def update_fields():

            if role_var.get() == "Warden":

                dep_label.pack_forget()
                dep_entry.pack_forget()
                id_label.config(text="UserID")

            else:

                dep_label.pack(anchor="w")
                dep_entry.pack(pady=5, ipady=6)
                id_label.config(text="Roll No")

        tk.Radiobutton(role_frame, text="Student",
                       variable=role_var, value="Student",
                       command=update_fields,
                       bg="#FFE4F1").pack(side="left", padx=15)

        tk.Radiobutton(role_frame, text="Warden",
                       variable=role_var, value="Warden",
                       command=update_fields,
                       bg="#FFE4F1").pack(side="left", padx=15)

        def signup():

            user = username_entry.get()
            dep = dep_entry.get()
            uid = id_entry.get()
            phone = phone_entry.get()
            pwd = password_entry.get()

            if user == "" or pwd == "":
                show_msg("Fill all fields", "#E53935")
                return

            cursor.execute(
                "SELECT * FROM users WHERE username=?", (user,))
            if cursor.fetchone():
                show_msg("User already exists", "#E53935")
                return

            if role_var.get() == "Student":

                cursor.execute(
                    "INSERT INTO users(username,password,role,department,roll_no,phone,year) VALUES(?,?,?,?,?,?,?)",
                    (user, pwd, "Student", dep, uid, phone,year_var.get()))

            else:

                cursor.execute(
                    "INSERT INTO users(username,password,role,userid,phone) VALUES(?,?,?,?,?)",
                    (user, pwd, "Warden", uid, phone))

            conn.commit()

            show_msg("Account Created")

            root.after(2000, show_login)

        tk.Button(card, text="SIGN UP",
                  command=signup,
                  bg="#D81B60",
                  fg="white",
                  width=22,
                  font=("Arial", 12, "bold")).pack(pady=12, ipady=6)

        tk.Button(card, text="Back to Login",
                  command=show_login,
                  bg="#BA68C8",
                  fg="white",
                  width=22,
                  font=("Arial", 12, "bold")).pack(ipady=6, pady=5)

    show_login()