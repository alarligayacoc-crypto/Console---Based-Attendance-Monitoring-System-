"""Console Based Attendance Monitoring System"""
from datetime import date, datetime

# ---------- SETTINGS ----------
DATE_FORMAT = "%Y-%m-%d"
NAME_WIDTH = 20
ID_WIDTH = 14

# ---------- DATA STRUCTURES ----------
# students: list of dicts {"id": int, "name": str}
students = [
    {"id": 22627015162, "name": "Sample Student"},
]

# attendance_records: [student_id, status_number, remarks_number or None, "YYYY‑MM‑DD"]
# Present students have no remarks (remarks_number is None).
# Many records per student, but only one per student per date.
attendance_records = [
    [22627015162, 2, 2, "2026‑10‑06"],
]

STATUS_LABELS = {1: "Present", 2: "Absent", 3: "Late"}
REMARK_LABELS = {1: "No remarks", 2: "Had a fever", 3: "Family emergency",
                 4: "Traffic", 5: "Other"}
NO_RECORD_TEXT = "No record"
PRESENT = 1
NO_REMARKS_TEXT = "-"  # shown in place of remarks for Present students


# ---------- DISPLAY HELPERS ----------
def print_title(text, width=75, char="="):
    print("\n" + char * width)
    print(text.center(width))
    print(char * width)


def short(text, width=NAME_WIDTH):
    return text if len(text) <= width else text[:width - 1] + "…"


def success(message):
    print(f"\n[SUCCESS] {message}")


def error(message):
    print(f"\n[ERROR] {message}")


# ---------- INPUT HELPERS ----------
def read_int(prompt):
    while True:
        value = input(prompt).strip()
        if value.isdigit():
            return int(value)
        print("[ERROR] Please enter a number.")


def read_optional_int(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            return None
        if value.isdigit():
            return int(value)
        print("[ERROR] Please enter a number or leave it blank.")


def is_valid_name(value):
    cleaned = value.replace(" ", "").replace(".", "").replace("-", "").replace("'", "")
    return cleaned.isalpha()


def read_name(prompt):
    while True:
        value = " ".join(input(prompt).split())
        if value and is_valid_name(value):
            return value.title()
        print("[ERROR] Please enter a valid name (letters only).")


def read_optional_name(prompt):
    while True:
        value = " ".join(input(prompt).split())
        if value == "":
            return None
        if is_valid_name(value):
            return value.title()
        print("[ERROR] Please enter a valid name (letters only) or leave it blank.")


def read_date(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":
            return date.today().strftime(DATE_FORMAT)
        try:
            parsed = datetime.strptime(value, DATE_FORMAT).date()
        except ValueError:
            print("[ERROR] Use the format YYYY‑MM‑DD (e.g. 2026‑10‑06).")
            continue
        if parsed > date.today():
            print("[ERROR] The date cannot be in the future.")
            continue
        return parsed.strftime(DATE_FORMAT)


def read_choice(prompt, labels):
    print(f"\n{prompt}:")
    for number, label in labels.items():
        print(f"  {number}. {label}")
    while True:
        value = read_int("Enter number: ")
        if value in labels:
            return value
        print(f"[ERROR] Please enter a number from 1 to {len(labels)}.")


# ---------- DATA HELPERS ----------
def find_student(student_id):
    for s in students:
        if s["id"] == student_id:
            return s
    return None


def find_record(student_id, att_date):
    for r in attendance_records:
        if r[0] == student_id and r[3] == att_date:
            return r
    return None


def remark_text(record):
    if record[1] == PRESENT or record[2] is None:
        return NO_REMARKS_TEXT
    return REMARK_LABELS[record[2]]


def get_status_and_remarks(student_id, att_date):
    record = find_record(student_id, att_date)
    if record is None:
        return NO_RECORD_TEXT, NO_RECORD_TEXT
    return STATUS_LABELS[record[1]], remark_text(record)


# ---------- FEATURE: STUDENT REGISTRATION ----------
def register_student(new_id, new_name):
    if find_student(new_id) is not None:
        error("Student ID already exists.")
        return
    students.append({"id": new_id, "name": new_name})
    success(f"New student record created for ID: {new_id} ({new_name})")


# ---------- FEATURE: EDIT STUDENT ----------
def edit_student(student_id):
    student = find_student(student_id)
    if student is None:
        error("Student ID not found!")
        return

    print(f"\nEditing Student -> ID: {student['id']}, Name: {student['name']}")
    new_id = read_optional_int("New Student ID (leave blank to keep current): ")
    new_name = read_optional_name("New Student Name (leave blank to keep current): ")

    if new_id is not None and new_id != student_id and find_student(new_id) is not None:
        error("That Student ID is already taken by another student.")
        return

    old_id = student["id"]
    if new_id is not None:
        student["id"] = new_id
        for record in attendance_records:
            if record[0] == old_id:
                record[0] = new_id
    if new_name is not None:
        student["name"] = new_name

    success(f"Student record updated -> ID: {student['id']}, Name: {student['name']}")


# ---------- FEATURE: REMOVE STUDENT ----------
def remove_student(student_id):
    global attendance_records
    student = find_student(student_id)
    if student is None:
        error("Student ID not found!")
        return

    confirm = input(f"Are you sure you want to remove {student['name']} "
                    f"({student_id}) and all their records? (y/n): ").strip().lower()
    if confirm != "y":
        print("\n[CANCELLED] Student was not removed.")
        return

    students.remove(student)
    attendance_records = [r for r in attendance_records if r[0] != student_id]
    success(f"Student {student_id} has been removed.")


# ---------- FEATURE: MARK ATTENDANCE ----------
def show_student_list(att_date=None):
    width = 62 if att_date else 40
    print("\n" + "-" * width)
    if att_date:
        print(f"ATTENDANCE DATE: {att_date}")
        print("-" * width)
        print(f"{'STUDENT ID':<{ID_WIDTH}} | {'STUDENT NAME':<{NAME_WIDTH}} | {'STATUS ON DATE':<14}")
    else:
        print(f"{'STUDENT ID':<{ID_WIDTH}} | {'STUDENT NAME':<{NAME_WIDTH}}")
    print("-" * width)
    if not students:
        print("No registered students.")
    for s in students:
        if att_date:
            status, _ = get_status_and_remarks(s["id"], att_date)
            print(f"{s['id']:<{ID_WIDTH}} | {short(s['name']):<{NAME_WIDTH}} | {status:<14}")
        else:
            print(f"{s['id']:<{ID_WIDTH}} | {short(s['name']):<{NAME_WIDTH}}")
    print("-" * width)


def mark_attendance(student_id, status, remarks, att_date):
    if status == PRESENT:
        remarks = None
    student = find_student(student_id)
    if student is None:
        error("Student ID not found!")
        return

    record = find_record(student_id, att_date)
    if record is None:
        attendance_records.append([student_id, status, remarks, att_date])
        action = "marked"
    else:
        record[1] = status
        record[2] = remarks
        action = "updated (a record already existed for this date)"

    success(f"Attendance {action}")
    print(f"Student ID   : {student['id']}")
    print(f"Student Name : {student['name']}")
    print(f"Date         : {att_date}")
    print(f"Status       : {STATUS_LABELS[status]}")
    if remarks is not None:
        print(f"Remarks      : {REMARK_LABELS[remarks]}")


def mark_attendance_flow():
    att_date = read_date("Attendance date (YYYY‑MM‑DD, blank for today): ")
    show_student_list(att_date)
    student_id = read_int("Enter Student ID to mark: ")
    student = find_student(student_id)
    if student is None:
        error("Student ID not found!")
        return
    header = f"{student['name']} (ID: {student['id']}) on {att_date}"
    status = read_choice(f"Attendance Status for {header}", STATUS_LABELS)
    remarks = None
    if status != PRESENT:
        remarks = read_choice(f"Remarks for {header}", REMARK_LABELS)
    mark_attendance(student_id, status, remarks, att_date)


# ---------- REPORTS ----------
def display_attendance_report(att_date):
    print_title(f"DAILY ATTENDANCE REPORT - {att_date}")
    print(f"{'STUDENT ID':<{ID_WIDTH}} | {'STUDENT NAME':<{NAME_WIDTH}} | {'STATUS':<10} | {'REMARKS':<16}")
    print("-" * 75)
    if not students:
        print("No registered students.")

    counts = {n: 0 for n in STATUS_LABELS}
    not_marked = 0
    for s in students:
        record = find_record(s["id"], att_date)
        status, remarks = get_status_and_remarks(s["id"], att_date)
        if record is None:
            not_marked += 1
        else:
            counts[record[1]] += 1
        print(f"{s['id']:<{ID_WIDTH}} | {short(s['name']):<{NAME_WIDTH}} | {status:<10} | {remarks:<16}")

    print("-" * 75)
    summary = "  ".join(f"{STATUS_LABELS[n]}: {c}" for n, c in counts.items())
    print(f"Summary -> {summary}  Not marked: {not_marked}")
    print("=" * 75)
    input("\nPress Enter to continue…")


def display_student_history(student_id):
    student = find_student(student_id)
    if student is None:
        error("Student ID not found!")
        return

    records = sorted((r for r in attendance_records if r[0] == student_id),
                     key=lambda r: r[3])

    print_title(f"ATTENDANCE HISTORY - {student['name']} (ID: {student['id']})", 60)
    print(f"{'DATE':<12} | {'STATUS':<10} | {'REMARKS':<16}")
    print("-" * 60)
    if not records:
        print("No attendance records yet.")
    for r in records:
        print(f"{r[3]:<12} | {STATUS_LABELS[r[1]]:<10} | {remark_text(r):<16}")
    print("-" * 60)
    if records:
        counts = {n: 0 for n in STATUS_LABELS}
        for r in records:
            counts[r[1]] += 1
        summary = ", ".join(f"{STATUS_LABELS[n]}: {c}" for n, c in counts.items())
        print(f"Total days: {len(records)} | {summary}")
    print("=" * 60)
    input("\nPress Enter to continue…")


# ---------- STUDENT‑ONLY VIEW ----------
def student_view():
    print_title("STUDENT ATTENDANCE VIEW", 60)
    sid = read_int("Enter your Student ID: ")
    name_input = read_name("Enter your Full Name: ")
    student = find_student(sid)
    if student is None or student["name"].strip().lower() != name_input.strip().lower():
        error("ID and name do not match our records.")
        input("Press Enter to continue…")
        return
    display_student_history(sid)
    print("\nThank you for checking your records.")
    input("Press Enter to go back to role selection…")


# ---------- TEACHER MENU ----------
def teacher_menu():
    while True:
        print("\n===== TEACHER MENU =====")
        print("1. Register Student")
        print("2. Mark Attendance")
        print("3. Edit Student")
        print("4. Remove Student")
        print("5. Daily Attendance Report")
        print("6. Student Attendance History")
        print("7. Go back to Role Selection")
        print("0. Exit")
        print("="*30)

        choice = read_int("Choose: ")
        if choice == 1:
            new_id = read_int("New Student ID (numbers only): ")
            new_name = read_name("New Student Name: ")
            register_student(new_id, new_name)
        elif choice == 2:
            mark_attendance_flow()
        elif choice == 3:
            edit_student(read_int("Student ID to edit: "))
        elif choice == 4:
            remove_student(read_int("Student ID to remove: "))
        elif choice == 5:
            display_attendance_report(read_date("Report date (YYYY‑MM‑DD, blank for today): "))
        elif choice == 6:
            show_student_list()
            display_student_history(read_int("Enter Student ID: "))
        elif choice == 7:
            print("\n↩ Going back to role selection…")
            break
        elif choice == 0:
            print("\nGoodbye!")
            exit()
        else:
            error("Invalid choice.")
        input("\nPress Enter to continue…")


# ---------- ROLE SELECTION + MAIN LOOP ----------
def main():
    while True:
        print_title("ATTENDANCE MONITORING SYSTEM — ROLE SELECT", 60)
        print("  1. I am a TEACHER")
        print("  2. I am a STUDENT")
        print("  0. Exit")
        print("="*60)
        role = read_int("Select your role: ")
        if role == 1:
            teacher_menu()
        elif role == 2:
            student_view()
        elif role == 0:
            print("\nGoodbye!")
            break
        else:
            error("Invalid choice, try again.")
            input("Press Enter to continue…")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nProgram closed. Goodbye!")