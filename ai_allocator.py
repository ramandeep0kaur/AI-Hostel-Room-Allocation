from database import connect_db

def compatibility_score(s1, s2):
    score = 0

    # study time match
    if s1[2] == s2[2]:
        score += 2

    # smoking habit match
    if s1[3] == s2[3]:
        score += 2

    # cleanliness match
    if s1[4] == s2[4]:
        score += 2

    # same year bonus
    if s1[1] == s2[1]:
        score += 1

    return score


def allocate_rooms():

    conn, cursor = connect_db()

    # ---------------- GET STUDENTS ----------------
    cursor.execute("""
    SELECT username, year, study_time, smoking, cleanliness
    FROM users
    WHERE role='Student'
    """)
    students = cursor.fetchall()

    students = list(students)

    # ---------------- GET ROOMS ----------------
    cursor.execute("SELECT room_no, capacity FROM rooms")
    rooms = cursor.fetchall()

    # Track allocation
    allocated = set()

    for room in rooms:

        room_no = room[0]
        capacity = room[1]

        room_students = []

        for s1 in students:

            if s1[0] in allocated:
                continue

            room_students.append(s1)
            allocated.add(s1[0])

            if len(room_students) == capacity:
                break

            # find best match for roommate
            best_match = None
            best_score = -1

            for s2 in students:

                if s2[0] in allocated:
                    continue

                score = compatibility_score(s1, s2)

                if score > best_score:
                    best_score = score
                    best_match = s2

            if best_match:
                room_students.append(best_match)
                allocated.add(best_match[0])

            if len(room_students) == capacity:
                break

        # ---------------- SAVE TO DATABASE ----------------
        bed_no = 1

        for student in room_students:

            username = student[0]

            cursor.execute("""
            INSERT INTO room_requests
            (username,room_no,bed_no,reason,status)
            VALUES(?,?,?,?,?)
            """,
            (username, room_no, str(bed_no), "AI Roommate Matching", "Approved"))

            cursor.execute("""
            UPDATE users
            SET room_no=?
            WHERE username=?
            """,
            (room_no, username))

            bed_no += 1

    conn.commit()
    conn.close()

    return "AI Roommate Allocation Completed"