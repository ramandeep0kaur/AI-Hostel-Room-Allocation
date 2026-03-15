import tkinter as tk
from tkinter import messagebox, ttk
from database import connect_db

def open_student(root, username, from_page=None):
    for w in root.winfo_children():
        w.destroy()

    root.geometry("1100x700")
    root.configure(bg="#F3E8FF")

    page_stack = []

    # ---------------- DATABASE TABLES ----------------
    conn, cursor = connect_db()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS room_requests(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        room_no TEXT,
        bed_no TEXT,
        reason TEXT,
        status TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS complaints(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        complaint TEXT,
        category TEXT,
        status TEXT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS notifications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT
    )
    """)
    
    conn.commit()
    conn.close()

    # ---------------- TOP BAR ----------------
    top = tk.Frame(root, bg="#D81B60", height=60)
    top.pack(fill="x")

    def smart_back():
        if from_page == "warden":
            from warden_panel import open_warden
            open_warden(root)
        else:
            from login_screen import login_screen
            login_screen(root)

    # NEW BACK LOGIC
    def go_back():
        if len(page_stack) > 1:
            page_stack.pop()
            page_stack[-1]()
        else:
            smart_back()

    back_btn = tk.Button(
        top, text="← Back", command=go_back, bg="white", fg="#D81B60",
        relief="flat", font=("Arial", 10, "bold")
    )
    back_btn.pack(side="left", padx=10, pady=10)

    title_label = tk.Label(
        top, text=f"Student Dashboard - {username}",
        font=("Arial", 18, "bold"), fg="white", bg="#D81B60"
    )
    title_label.pack(side="left", padx=20)

    from login_screen import login_screen
    logout_btn = tk.Button(
        top, text="Logout", command=lambda: login_screen(root),
        bg="white", fg="#D81B60", relief="flat", font=("Arial", 10, "bold")
    )
    logout_btn.pack(side="right", padx=20, pady=10)

    # ---------------- MAIN AREA ----------------
    main = tk.Frame(root, bg="#F3E8FF")
    main.pack(expand=True, fill="both", side="right")

    def clear_main():
        for w in main.winfo_children():
            w.destroy()

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

    hamburger_btn = tk.Button(
        hamburger_frame, text="☰", font=("Arial", 16, "bold"),
        bg="white", fg="#D81B60", relief="flat", command=toggle_menu
    )
    hamburger_btn.pack(pady=10, padx=5)

    # ---------------- DASHBOARD ----------------
    def dashboard():
        clear_main()
        if not page_stack or page_stack[-1] != dashboard:
            page_stack.append(dashboard)

        container = tk.Frame(main, bg="#F3E8FF")
        container.pack(pady=60, fill="both", expand=True)

        tk.Label(container, text="🏠 Student Dashboard", font=("Arial", 24, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        cards = tk.Frame(container, bg="#F3E8FF")
        cards.pack(pady=60)

        def card(title_text, value_text):
            c = tk.Frame(cards, bg="white", width=200, height=120, bd=2, relief="ridge")
            c.pack(side="left", padx=20)
            tk.Label(c, text=title_text, font=("Arial", 14, "bold"), bg="white").pack(pady=10)
            tk.Label(c, text=value_text, font=("Arial", 18, "bold"), fg="#D81B60", bg="white").pack()

        conn, cursor = connect_db()
        cursor.execute("SELECT room_no FROM users WHERE username=?", (username,))
        data = cursor.fetchone()
        room = data[0] if data and data[0] else "Not Assigned"

        cursor.execute("SELECT status FROM room_requests WHERE username=? ORDER BY id DESC LIMIT 1", (username,))
        req = cursor.fetchone()
        status = req[0] if req else "No Request"
        conn.close()

        card("Your Room", room)
        card("Last Request Status", status)
        card("Notifications", "Check Panel")

    # ---------------- PROFILE ----------------
    def view_info():
        clear_main()
        if not page_stack or page_stack[-1] != view_info:
            page_stack.append(view_info)

        conn, cursor = connect_db()
        cursor.execute(
            "SELECT username, roll_no, department, year, phone, room_no FROM users WHERE username=?",
            (username,)
        )
        data = cursor.fetchone()
        conn.close()

        labels = ["Username", "Roll No", "Department", "Year", "Phone", "Room"]

        card = tk.Frame(main, bg="white", padx=40, pady=35, bd=2, relief="ridge")
        card.pack(pady=70)
  
        tk.Label(card, text="👤 Student Profile",
                 font=("Arial",22,"bold"), fg="#BA68C8", bg="white").pack(pady=10)

        for label, value in zip(labels, data):
            row = tk.Frame(card, bg="white")
            row.pack(anchor="w", pady=6)

            tk.Label(row, text=f"{label} :", font=("Arial",13,"bold"),
                     width=12, anchor="w", bg="white").pack(side="left")

            tk.Label(row, text=value if value else "Not Assigned",
                     font=("Arial",13), bg="white").pack(side="left")

    # ---------------- VACANT ROOMS ----------------
    def view_rooms():
        clear_main()
        if not page_stack or page_stack[-1] != view_rooms:
            page_stack.append(view_rooms)

        tk.Label(main, text="🏢 Vacant Rooms", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        canvas = tk.Canvas(main, bg="#F3E8FF", highlightthickness=0)
        scrollbar = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F3E8FF")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        def _on_mousewheel(event):
            if canvas.winfo_exists():
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        conn, cursor = connect_db()
        cursor.execute("SELECT room_no, capacity, floor, beds FROM rooms")
        rooms = cursor.fetchall()
        conn.close()

        max_columns = 3
        row = 0
        col = 0

        for room in rooms:
            room_no, capacity_val, floor, beds = room

            occupied_beds = []
            if beds:
                occupied_beds = [int(b) for b in beds.split(",") if b]

            # REMOVE PENDING/APPROVED REQUEST BEDS
            conn2, cur2 = connect_db()
            cur2.execute(
                "SELECT bed_no FROM room_requests WHERE room_no=? AND status IN ('Pending','Approved')",
                (room_no,))
            extra = cur2.fetchall()
            conn2.close()

            for e in extra:
                occupied_beds.append(int(e[0]))

            available_beds = [b for b in range(1, int(capacity_val)+1) if b not in occupied_beds]
            available = len(available_beds) > 0

            card_frame = tk.Frame(scroll_frame, bg="white", bd=2, relief="ridge", padx=20, pady=15, width=250, height=200)
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="n")

            tk.Label(card_frame, text=f"Room No: {room_no}", font=("Arial", 14, "bold"), bg="white").pack(anchor="w")
            tk.Label(card_frame, text=f"Floor: {floor}", font=("Arial", 13, "bold"), bg="white").pack(anchor="w")
            tk.Label(card_frame, text=f"Capacity: {capacity_val}", font=("Arial", 13, "bold"), bg="white").pack(anchor="w")
            tk.Label(card_frame, text=f"Available Beds: {', '.join(map(str, available_beds)) if available else 'Full'}",
                     font=("Arial", 13, "bold"), bg="white").pack(anchor="w")

            tk.Label(card_frame, text="Select Bed:", bg="white").pack()
            bed_selection = ttk.Combobox(card_frame, values=available_beds, width=5)
            bed_selection.pack(pady=5)

            def send_request(r=room_no, b=bed_selection):
                if not b.get():
                    messagebox.showerror("Error", "Select a bed number")
                    return

                conn, cursor = connect_db()

                cursor.execute("SELECT * FROM room_requests WHERE username=? AND status='Pending'", (username,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "You already have a pending request")
                    conn.close()
                    return

                cursor.execute(
                    "INSERT INTO room_requests(username,room_no,bed_no,reason,status) VALUES(?,?,?,?,?)",
                    (username, r, b.get(), "Requested from vacant room list", "Pending")
                )

                cursor.execute(
                    "INSERT INTO notifications(username,message) VALUES(?,?)",
                    (username, f"Room request sent for Room {r}, Bed {b.get()}")
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Success", f"Request sent for Room {r}, Bed {b.get()}")

                view_rooms()

            tk.Button(card_frame, text="Request", bg="#BA68C8", fg="white",
                      font=("Arial", 12, "bold"),
                      command=send_request,
                      state=tk.NORMAL if available else tk.DISABLED).pack(pady=5)

            col += 1
            if col >= max_columns:
                col = 0
                row += 1
    
    # ---------------- ROOMMATE PREFERENCES ----------------
    def preferences(): 
        clear_main()

        if not page_stack or page_stack[-1] != preferences:
            page_stack.append(preferences)

        tk.Label(
            main,
            text="🤝 Roommate Preferences",
            font=("Arial",22,"bold"),
            bg="#F3E8FF",
            fg="#BA68C8"
        ).pack(pady=20)

        card = tk.Frame(main, bg="white", padx=40, pady=40, bd=2, relief="ridge")
        card.pack(pady=40)

        # Study Time
        tk.Label(card, text="Study Time", bg="white").pack()
        study_var = tk.StringVar()

        ttk.Combobox(
            card,
            textvariable=study_var,
            values=["Morning","Night"],
            width=20
        ).pack(pady=5)

        # Smoking
        tk.Label(card, text="Smoking", bg="white").pack()
        smoke_var = tk.StringVar()

        ttk.Combobox(
            card,
            textvariable=smoke_var,
            values=["Yes","No"],
            width=20
        ).pack(pady=5)

        # Cleanliness
        tk.Label(card, text="Cleanliness", bg="white").pack()
        clean_var = tk.StringVar()

        ttk.Combobox(
            card,
            textvariable=clean_var,
            values=["Low","Medium","High"],
            width=20
        ).pack(pady=5)

        # Year
        tk.Label(card, text="Year", bg="white").pack()
        year_var = tk.IntVar()

        ttk.Combobox(
            card,
            textvariable=year_var,
            values=[1,2,3,4],
            width=20
        ).pack(pady=5)

        def save_preferences():
            
            conn, cursor = connect_db()

            cursor.execute("""
            UPDATE users
            SET study_time=?, smoking=?, cleanliness=?, year=?
            WHERE username=?
            """,
            (
                study_var.get(),
                smoke_var.get(),
                clean_var.get(),
                year_var.get(),
                username
            ))

            conn.commit()
            conn.close()

            messagebox.showinfo("Saved", "Preferences saved successfully")

        tk.Button(
            card,
            text="Save Preferences",
            bg="#BA68C8",
            fg="white",
            font=("Arial",12,"bold"),
            command=save_preferences
        ).pack(pady=15)
    # ---------------- COMPLAINT PANEL ----------------
    def complaint_panel():
        clear_main()
        if not page_stack or page_stack[-1] != complaint_panel:
            page_stack.append(complaint_panel)

        tk.Label(main, text="🛏 Submit Complaint", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        card = tk.Frame(main, bg="#FFF0F7", padx=40, pady=40, bd=2, relief="ridge")
        card.pack()

        tk.Label(card, text="Complaint type", bg="#FFF0F7").pack()
        categories = ["Electricity", "Water", "Furniture", "Other"]
        category_box = ttk.Combobox(card, values=categories, width=25)
        category_box.pack(pady=5)
        category_box.current(0)

        tk.Label(card, text="Your Complaint", bg="#FFF0F7").pack()
        complaint_text = tk.Text(card, width=35, height=5)
        complaint_text.pack(pady=5)

        def submit_complaint():
            text = complaint_text.get("1.0", "end").strip()
            category = category_box.get()

            if text == "":
                messagebox.showerror("Error", "Enter a complaint")
                return

            conn, cursor = connect_db()

            cursor.execute(
                "INSERT INTO complaints(username, complaint, category, status) VALUES(?,?,?,?)",
                (username, text, category, "Pending")
            )

            cursor.execute(
                "INSERT INTO notifications(username,message) VALUES(?,?)",
                (username, f"{category} complaint submitted successfully")
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Complaint submitted")

            complaint_text.delete("1.0", "end")
            category_box.current(0)

        tk.Button(card, text="Submit Complaint", bg="#BA68C8", fg="white",
                  font=("Arial", 12, "bold"), width=20, command=submit_complaint).pack(pady=15)

    # ---------------- NOTIFICATIONS ----------------
    def notifications():
        clear_main()
        if not page_stack or page_stack[-1] != notifications:
            page_stack.append(notifications)

        tk.Label(main, text="🔔 Notifications", font=("Arial", 22, "bold"),
                 bg="#F3E8FF", fg="#BA68C8").pack(pady=20)

        canvas = tk.Canvas(main, bg="#F3E8FF", highlightthickness=0)
        scrollbar = tk.Scrollbar(main, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg="#F3E8FF")

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        conn, cursor = connect_db()

        cursor.execute("""
        SELECT message 
        FROM notifications 
        WHERE username=? 
        ORDER BY id DESC
        """, (username,))

        rows = cursor.fetchall()
        conn.close()

        for r in rows:
            card = tk.Frame(scroll_frame, bg="#E1BEE7", bd=1, relief="ridge", padx=10, pady=10)
            card.pack(fill="x", pady=5)

            tk.Label(card, text=r[0], font=("Arial", 12, "bold"),
                     bg="#E1BEE7", fg="#4A148C",
                     anchor="w", justify="left").pack(fill="x")

    # ---------------- SIDEBAR BUTTONS ----------------
    menu_items = [
        ("🏠 Dashboard", dashboard),
        ("👤 Profile", view_info),
        ("🏢 Vacant Rooms", view_rooms),
        ("🤝 Roommate Preferences", preferences),
        ("🛏 Complaints", complaint_panel),
        ("🔔 Notifications", notifications),
    ]

    for t, c in menu_items:
        tk.Button(menu_frame, text=t, width=22, bg="#BA68C8", fg="white",
                  font=("Arial", 12, "bold"), anchor="w", command=c).pack(pady=5, padx=10)

    dashboard()