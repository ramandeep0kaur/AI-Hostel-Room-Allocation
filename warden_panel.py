# warden_panel.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import connect_db
from ai_allocator import allocate_rooms

def open_warden(root, username="Warden"):

    for w in root.winfo_children():
        w.destroy()

    root.geometry("1100x700")
    root.configure(bg="#F3E8FF")

    page_stack = []

    # ---------------- TOP BAR ----------------
    top = tk.Frame(root, bg="#D81B60", height=60)
    top.pack(fill="x")
 
    def go_back():
        if len(page_stack) > 1:
           page_stack.pop()     
           page_stack[-1]()     
        else:
           from login_screen import login_screen
           login_screen(root)
    
    tk.Button(top, text="← Back", command=go_back, bg="white", fg="#D81B60",
              relief="flat", font=("Arial", 10, "bold")).pack(side="left", padx=10, pady=10)

    tk.Label(top, text="Warden Dashboard", font=("Arial", 18, "bold"),
             fg="white", bg="#D81B60").pack(side="left", padx=20)

    from login_screen import login_screen
    tk.Button(top, text="Logout", command=lambda: login_screen(root),
              bg="white", fg="#D81B60", relief="flat",
              font=("Arial", 10, "bold")).pack(side="right", padx=20, pady=10)

    # ---------------- MAIN AREA ----------------
    main = tk.Frame(root, bg="#F3E8FF")
    main.pack(expand=True, fill="both", side="right")

    def clear_main():
        for w in main.winfo_children():
            w.destroy()

    def push_page(func):
        # Only push if not already on stack top
        if not page_stack or page_stack[-1] != func:
            page_stack.append(func)

    # ---------------- SIDEBAR ----------------
    hamburger_frame = tk.Frame(root, bg="#F3E8FF", width=40)
    hamburger_frame.pack(side="left", fill="y")

    menu_frame = tk.Frame(root, bg="#BA68C8", width=180)
    menu_frame.pack(side="left", fill="y")

    def toggle_menu():
        if menu_frame.winfo_ismapped():
            menu_frame.pack_forget()
        else:
            menu_frame.pack(side="left", fill="y")

    tk.Button(hamburger_frame, text="☰", font=("Arial", 16, "bold"),
              bg="white", fg="#D81B60", relief="flat",
              command=toggle_menu).pack(pady=10, padx=5)

    # ---------------- DASHBOARD ----------------
    def dashboard():
        clear_main()
        push_page(dashboard)

        container = tk.Frame(main, bg="#F3E8FF")
        container.pack(pady=40)

        tk.Label(container,
                 text="🏢 Warden Dashboard",
                 font=("Arial",24,"bold"),
                 bg="#F3E8FF",
                 fg="#BA68C8").pack(pady=20)

        def run_allocator():
            from ai_allocator import allocate_rooms
            allocate_rooms()
            messagebox.showinfo("Success","AI Room Allocation Completed")

        tk.Button(
            container,
            text="🤖 Run AI Room Allocator",
            bg="#4CAF50",
            fg="white",
            font=("Arial",14,"bold"),
            padx=20,
            pady=10,
            command=run_allocator
        ).pack(pady=15)

        cards = tk.Frame(container, bg="#F3E8FF")
        cards.pack(pady=20)

        def card(title,value,color):
            c = tk.Frame(cards,bg="white",width=200,height=120,bd=2,relief="ridge")
            c.pack(side="left",padx=10)
            tk.Label(c,text=title,font=("Arial",14,"bold"),bg="white").pack(pady=10)
            tk.Label(c,text=value,font=("Arial",20,"bold"),fg=color,bg="white").pack()

        conn,cursor = connect_db()

        cursor.execute("SELECT COUNT(*) FROM users WHERE role='Student'")
        students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM rooms")
        rooms = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM room_requests WHERE status='Pending'")
        requests_count = cursor.fetchone()[0]

    # complaints
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Pending'")
        pending_complaints = cursor.fetchone()[0]
   
        cursor.execute("SELECT COUNT(*) FROM complaints WHERE status='Resolved'")
        resolved_complaints = cursor.fetchone()[0]

    # occupancy
        cursor.execute("SELECT COUNT(*) FROM room_requests WHERE status='Approved'")
        occupied = cursor.fetchone()[0]

    # department data
        try:
            cursor.execute("""
            SELECT department, COUNT(*)
            FROM users
            WHERE role='Student'
            GROUP BY department
            """)
            dept_data = cursor.fetchall()
        except:
            dept_data = []

        conn.close()

        card("Total Students",students,"#4CAF50")
        card("Total Rooms",rooms,"#2196F3")
        card("Pending Requests",requests_count,"#FF9800")
        card("Pending Complaints",pending_complaints,"#E91E63")
        card("Resolved Complaints",resolved_complaints,"#4CAF50")
        card("Occupied Rooms",occupied,"#9C27B0")
    
        dept_frame = tk.Frame(container,bg="#F3E8FF")
        dept_frame.pack(pady=30)

        tk.Label(
            dept_frame,
            text="📊 Department Wise Students",
            font=("Arial",18,"bold"),
            bg="#F3E8FF",
            fg="#6A1B9A"
        ).pack(pady=10)

        for dept,count in dept_data:
            
            box = tk.Frame(dept_frame,bg="white",bd=2,relief="ridge",width=220,height=70)
            box.pack(pady=5)

            tk.Label(box,text=dept,font=("Arial",14,"bold"),bg="white").pack()
            tk.Label(box,text=f"{count} Students",font=("Arial",13),fg="#4CAF50",bg="white").pack()

    # ---------------- ADD ROOM ----------------
    def add_room():
        clear_main()
        push_page(add_room)
        tk.Label(main, text="➕ Add New Room", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=30)

        card_frame = tk.Frame(main, bg="white", padx=40, pady=40, bd=2, relief="ridge")
        card_frame.pack()

        tk.Label(card_frame, text="Room Number", bg="white", font=("Arial", 12)).pack(anchor="w")
        room_no = tk.Entry(card_frame, width=30, font=("Arial", 12))
        room_no.pack(pady=5)

        tk.Label(card_frame, text="Floor", bg="white", font=("Arial", 12)).pack(anchor="w")
        floor = tk.Entry(card_frame, width=30, font=("Arial", 12))
        floor.pack(pady=5)

        tk.Label(card_frame, text="Seater (Capacity)", bg="white", font=("Arial", 12)).pack(anchor="w")
        capacity = ttk.Combobox(card_frame, values=[1, 2, 3, 4, 5], width=27, font=("Arial", 12))
        capacity.pack(pady=5)

        bed_frame = tk.Frame(card_frame, bg="white")
        bed_frame.pack(pady=10)
        bed_vars = []

        def generate_beds(event):
            for w in bed_frame.winfo_children():
                w.destroy()
            bed_vars.clear()
            c = capacity.get()
            if c == "":
                return
            for i in range(1, int(c) + 1):
                var = tk.IntVar()
                cb = tk.Checkbutton(bed_frame, text=f"Bed {i}", variable=var, bg="white", font=("Arial", 12))
                cb.pack(anchor="w")
                bed_vars.append((i, var))

        capacity.bind("<<ComboboxSelected>>", generate_beds)

        def save():
            r = room_no.get()
            f = floor.get()
            c = capacity.get()
            if r == "" or f == "" or c == "":
                messagebox.showerror("Error", "Fill all fields")
                return
            occupied = []
            for bed, var in bed_vars:
                if var.get() == 1:
                    occupied.append(str(bed))
            beds = ",".join(occupied)
            conn, cursor = connect_db()
            try:
                cursor.execute(
                    "INSERT INTO rooms(room_no,capacity,floor,beds) VALUES(?,?,?,?)",
                    (r, c, f, beds)
                )
                conn.commit()
                messagebox.showinfo("Success", "Room Added")
            except:
                messagebox.showerror("Error", "Room Number already exists!")
            conn.close()

        tk.Button(
            card_frame,
            text="Add Room",
            bg="#BA68C8",
            fg="white",
            font=("Arial", 14, "bold"),
            width=20,
            command=save
        ).pack(pady=15)

    # ---------------- VACANT ROOMS ----------------
    def vacant_rooms():
        clear_main()
        push_page(vacant_rooms)
        tk.Label(main, text="🏠 Vacant Rooms", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        tree_frame = tk.Frame(main)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 13), rowheight=30)

        tree = ttk.Treeview(tree_frame,
                            columns=("Room No", "Floor", "Capacity", "Available Beds"),
                            show="headings", height=15)
        tree.heading("Room No", text="Room No")
        tree.heading("Floor", text="Floor")
        tree.heading("Capacity", text="Capacity")
        tree.heading("Available Beds", text="Available Beds")
        tree.column("Room No", width=120, anchor="center")
        tree.column("Floor", width=120, anchor="center")
        tree.column("Capacity", width=120, anchor="center")
        tree.column("Available Beds", width=200, anchor="center")
        tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        conn, cursor = connect_db()
        cursor.execute("SELECT room_no, floor, capacity, beds FROM rooms")
        rooms_list = cursor.fetchall()
        cursor.execute("SELECT room_no, bed_no FROM room_requests WHERE status='Approved'")
        approved_requests = cursor.fetchall()
        conn.close()

        approved_dict = {}
        for room_no, bed_no in approved_requests:
            approved_dict.setdefault(room_no, []).append(int(bed_no))
        for r in rooms_list:
            room_no, floor, capacity_val, beds = r

            occupied_beds = [int(b) for b in beds.split(",") if b] if beds else []

            if room_no in approved_dict:
                occupied_beds.extend(approved_dict[room_no])

            available_beds = [
                str(b) for b in range(1, int(capacity_val) + 1)
                if b not in occupied_beds
    ]

            if not available_beds:
               bed_display = "Full"
            else:
               bed_display = ", ".join(available_beds)
            tree.insert(
                "",
                tk.END,
                values=(room_no, floor, capacity_val, bed_display)
            )

        btn_frame = tk.Frame(main, bg="#F3E8FF")
        btn_frame.pack(pady=10)

        def edit_room():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a room first")
                return
            room_no = selected[0]
            from edit_room_screen import edit_room_screen
            edit_room_screen(main, room_no)
            vacant_rooms()

        def delete_room():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Select a room first")
                return
            room_no = selected[0]
            if messagebox.askyesno("Confirm", f"Delete Room {room_no}?"):
                conn, cursor = connect_db()
                cursor.execute("DELETE FROM rooms WHERE room_no=?", (room_no,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", f"Room {room_no} deleted")
                vacant_rooms()

        tk.Button(btn_frame, text="Edit", bg="#FF9800", fg="white", width=15,
                  font=("Arial",12,"bold"), command=edit_room).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete", bg="#F44336", fg="white", width=15,
                  font=("Arial",12,""), command=delete_room).pack(side="left", padx=10)
    # ---------------- STUDENT LIST ----------------
    def student_list():
        clear_main()
        push_page(student_list)

        tk.Label(main, text="👨‍🎓 Student List",
                 font=("Arial",22,"bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=15)

        top = tk.Frame(main, bg="#F3E8FF")
        top.pack(pady=10)

    # SEARCH BOX
        search_var = tk.StringVar()
        tk.Entry(top, textvariable=search_var, width=25,
                 font=("Arial",12)).pack(side="left", padx=5)

    # DEPARTMENT FILTER
        dept_var = tk.StringVar()
        dept_box = ttk.Combobox(top, textvariable=dept_var,
                                values=["All","CSE","ECE","ME","CE","IT"],
                                width=10)
        dept_box.current(0)
        dept_box.pack(side="left", padx=5)

        table_frame = tk.Frame(main)
        table_frame.pack(pady=10)

        columns = ("Username","Roll No","Department","Year","Phone","Room")

        tree = ttk.Treeview(table_frame, columns=columns,
                        show="headings", height=15)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=140)

        tree.pack(side="left")

        scrollbar = ttk.Scrollbar(table_frame,
                                  orient="vertical",
                                  command=tree.yview)
        scrollbar.pack(side="right", fill="y")

        tree.configure(yscrollcommand=scrollbar.set)

    # LOAD DATA
        def load_students():
            for row in tree.get_children():
                tree.delete(row)

            conn, cursor = connect_db()

            query = """
            SELECT username, roll_no, department, year, phone, room_no
            FROM users WHERE role='Student'
            """

            cursor.execute(query)
            rows = cursor.fetchall()
            conn.close()

            for r in rows:
                tree.insert("", "end", values=r)

        load_students()

    # SEARCH
        def search_student():
            keyword = search_var.get()

            for row in tree.get_children():
                tree.delete(row)

            conn, cursor = connect_db()

            cursor.execute("""
            SELECT username, roll_no, department, year, phone, room_no
            FROM users
            WHERE role='Student' AND username LIKE ?
            """, ("%"+keyword+"%",))

            rows = cursor.fetchall()
            conn.close()

            for r in rows:
                tree.insert("", "end", values=r)

        tk.Button(top, text="🔍 Search",
                    bg="#4CAF50", fg="white",
                    command=search_student).pack(side="left", padx=5)

    # DELETE STUDENT
        def delete_student():
            selected = tree.focus()
   
            if not selected:
                messagebox.showwarning("Warning","Select a student")
                return

            values = tree.item(selected,"values")
            username = values[0]

            conn, cursor = connect_db()
            cursor.execute("DELETE FROM users WHERE username=?", (username,))
            conn.commit()
            conn.close()

            tree.delete(selected)

            messagebox.showinfo("Deleted","Student removed")

        tk.Button(main, text="❌ Delete Student",
                  bg="#F44336", fg="white",
                  font=("Arial",11,"bold"),
                  command=delete_student).pack(pady=10)

    # EDIT STUDENT
        def edit_student():
            selected = tree.focus()

            if not selected:
                messagebox.showwarning("Warning","Select a student")
                return

            values = tree.item(selected,"values")

            win = tk.Toplevel(root)
            win.title("Edit Student")
            win.geometry("350x350")

            labels = ["Username","Roll No","Department","Year","Phone"]

            entries = []

            for i,l in enumerate(labels):
                tk.Label(win,text=l).pack(pady=5)
                e = tk.Entry(win)
                e.insert(0,values[i])
                e.pack()
                entries.append(e)

            def update_student():
                
                conn,cursor = connect_db()
                cursor.execute("""
                UPDATE users
                SET roll_no=?, department=?, year=?, phone=?
                WHERE username=?
                """,(
                    entries[1].get(),
                    entries[2].get(),
                    entries[3].get(),
                    entries[4].get(),
                    entries[0].get()
                ))

                conn.commit()
                conn.close()

                messagebox.showinfo("Updated","Student updated")
                win.destroy()
            load_students()

            tk.Button(win,text="Update",
                      bg="#4CAF50", fg="white",
                      command=update_student).pack(pady=15)

            tk.Button(main, text="✏ Edit Student",
                      bg="#2196F3", fg="white",
                      font=("Arial",11,"bold"),
                      command=edit_student).pack()
    # ---------------- ROOM REQUESTS ----------------
    def requests():
        clear_main()
        push_page(requests)
        tk.Label(main, text="📨 Room Requests", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 13), rowheight=30)

        table = ttk.Treeview(main,
                             columns=("Student", "Room", "Bed", "Status"),
                             show="headings", height=15)

        table.heading("Student", text="Student")
        table.heading("Room", text="Room")
        table.heading("Bed", text="Bed")
        table.heading("Status", text="Status")
        table.column("Student", width=150, anchor="center")
        table.column("Room", width=100, anchor="center")
        table.column("Bed", width=100, anchor="center")
        table.column("Status", width=120, anchor="center")
        table.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        conn, cursor = connect_db()
        cursor.execute(
            "SELECT username, room_no, bed_no, status FROM room_requests"
        )
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            table.insert("", tk.END, values=r)

        btn_frame = tk.Frame(main, bg="#F3E8FF")
        btn_frame.pack(pady=10)

        def approve_request():
            selected = table.selection()
            if not selected:
                messagebox.showerror("Error", "Select a request first")
                return
            item = table.item(selected[0])
            username, room_no, bed_no, status = item["values"]
            if status == "Approved":
                messagebox.showinfo("Info", "Request already approved")
                return
            conn, cursor = connect_db()
            cursor.execute(
                "UPDATE room_requests SET status='Approved' WHERE username=? AND room_no=? AND bed_no=?",
                (username, room_no, bed_no)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Request Approved")
            vacant_rooms()
            requests()

        def reject_request():
            selected = table.selection()
            if not selected:
                messagebox.showerror("Error", "Select a request first")
                return
            item = table.item(selected[0])
            username, room_no, bed_no, status = item["values"]
            if status == "Rejected":
                messagebox.showinfo("Info", "Request already rejected")
                return
            conn, cursor = connect_db()
            cursor.execute(
                "UPDATE room_requests SET status='Rejected' WHERE username=? AND room_no=? AND bed_no=?",
                (username, room_no, bed_no)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Request Rejected")
            vacant_rooms()
            requests()

        def delete_request():
            selected = table.selection()
            if not selected:
                messagebox.showerror("Error", "Select a request first")
                return
            item = table.item(selected[0])
            username, room_no, bed_no, status = item["values"]
            if messagebox.askyesno("Confirm", f"Delete request of {username} for Room {room_no}, Bed {bed_no}?"):
                conn, cursor = connect_db()
                cursor.execute(
                    "DELETE FROM room_requests WHERE username=? AND room_no=? AND bed_no=?",
                    (username, room_no, bed_no)
                )
                conn.commit()
                conn.close()
                messagebox.showinfo("Deleted", "Request deleted")
                vacant_rooms()
                requests()

        tk.Button(btn_frame, text="Approve", bg="#4CAF50", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=approve_request).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Reject", bg="#F44336", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=reject_request).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete", bg="#FF9800", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=delete_request).pack(side="left", padx=10)

    # ---------------- COMPLAINTS ----------------
    def complaints():
        clear_main()
        push_page(complaints)
        tk.Label(main, text="📝 Student Complaints", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 14, "bold"))
        style.configure("Treeview", font=("Arial", 13), rowheight=30)

        table = ttk.Treeview(main,
                             columns=("Student", "Type", "Description", "Status"),
                             show="headings", height=15)

        table.heading("Student", text="Student")
        table.heading("Type", text="Type")
        table.heading("Description", text="Description")
        table.heading("Status", text="Status")

        table.column("Student", width=150, anchor="center")
        table.column("Type", width=120, anchor="center")
        table.column("Description", width=300, anchor="w")
        table.column("Status", width=120, anchor="center")
        table.pack(fill="both", expand=True, padx=20, pady=20)

        scrollbar = ttk.Scrollbar(main, orient="vertical", command=table.yview)
        table.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        conn, cursor = connect_db()
        cursor.execute("SELECT username, category, complaint, status FROM complaints")
        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            table.insert("", tk.END, values=r)

        btn_frame = tk.Frame(main, bg="#F3E8FF")
        btn_frame.pack(pady=10)

        def set_status(new_status):
            selected = table.selection()
            if not selected:
                messagebox.showerror("Error", "Select a complaint first")
                return
            item = table.item(selected[0])
            username, ctype, desc, status = item["values"]
            conn, cursor = connect_db()
            cursor.execute(
                "UPDATE complaints SET status=? WHERE username=? AND category=? AND complaint=?",
                (new_status, username, ctype, desc)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Complaint marked as {new_status}")
            complaints()

        def delete_complaint():
            selected = table.selection()
            if not selected:
                messagebox.showerror("Error", "Select a complaint first")
                return
            item = table.item(selected[0])
            username, ctype, desc, status = item["values"]
            if messagebox.askyesno("Confirm", f"Delete complaint from {username}?"):
                conn, cursor = connect_db()
                cursor.execute(
                   "DELETE FROM complaints WHERE username=? AND category=? AND complaint=?",
                    (username, ctype, desc)
                )
                cursor.execute(
                   "INSERT INTO notifications(username,message,status) VALUES(?,?,?)",
                (username, f"Your complaint '{desc}' has been deleted by Warden", "Unread")
            )

        tk.Button(btn_frame, text="Not Yet", bg="#5A5A5A", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=lambda: set_status("Not Yet")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="In Progress", bg="#FF9800", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=lambda: set_status("In Progress")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Completed", bg="#4CAF50", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=lambda: set_status("Completed")).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Delete", bg="#2196F3", fg="white", width=15,
                  font=("Arial", 12, "bold"), command=delete_complaint).pack(side="left", padx=10)

    # ---------------- NOTIFICATIONS ----------------
    def notifications():
        clear_main()
        push_page(notifications)
        tk.Label(main, text="🔔 Send Notification", font=("Arial", 24, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        card = tk.Frame(main, bg="#E1BEE7", padx=50, pady=50, bd=3, relief="ridge")
        card.pack(pady=20)

        tk.Label(card, text="Select Student", font=("Arial", 14, "bold"), bg="#E1BEE7").pack(anchor="w", pady=5)
        conn, cursor = connect_db()
        cursor.execute("SELECT username FROM users WHERE role='student'")
        students = [r[0] for r in cursor.fetchall()]
        conn.close()
        students.insert(0, "All Students")

        student_cb = ttk.Combobox(card, values=students, width=40, font=("Arial", 12))
        student_cb.pack(pady=5)

        tk.Label(card, text="Notification Message", font=("Arial", 14, "bold"), bg="#E1BEE7").pack(anchor="w", pady=5)
        message_text = tk.Text(card, width=60, height=8, font=("Arial", 12), bg="#F3E5F5")
        message_text.pack(pady=5)

        def send_notification():
            student = student_cb.get()
            message = message_text.get("1.0", "end").strip()
            if not student or not message:
                messagebox.showerror("Error", "Select student and write message")
                return

            conn, cursor = connect_db()
            if student == "All Students":
                cursor.execute("SELECT username FROM users WHERE role='student'")
                all_students = [r[0] for r in cursor.fetchall()]
                for s in all_students:
                    cursor.execute(
                        "INSERT INTO notifications(username,message,status) VALUES(?,?,?)",
                        (s, message, "Unread")
                    )
            else:
                cursor.execute(
                    "INSERT INTO notifications(username,message,status) VALUES(?,?,?)",
                    (student, message, "Unread")
                )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sent", f"Notification sent successfully!")
            student_cb.set("")
            message_text.delete("1.0", "end")

        tk.Button(card, text="Send Notification", bg="#BA68C8", fg="white",
                  font=("Arial", 14, "bold"), width=30, command=send_notification).pack(pady=15)

    # ---------------- MENU BUTTONS ----------------
    menu_items = [
        ("🏠 Dashboard", dashboard),
        ("➕ Add Room", add_room),
        ("🏠 Vacant Rooms", vacant_rooms),
        ("👨‍🎓 Student List", student_list),
        ("📨 Room Requests", requests),
        ("📝 Complaints", complaints),
        ("🔔 Notifications", notifications),
    ]

    for text, command in menu_items:
        tk.Button(menu_frame, text=text, width=22, bg="#BA68C8",
                  fg="white", font=("Arial", 12, "bold"),
                  anchor="w", command=command).pack(pady=5, padx=10)

    dashboard()