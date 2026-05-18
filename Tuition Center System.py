# Brilliant Tuition Centre Management System

# Group Members and TP Numbers:
# 1. Ho Hooi Bin (TP082033)(STUDENT)
# 2. Jeremiah Lim Chen Kai (TP083352)(ADMIN)
# 3. Teoh Qiao Hui (TP083838)(TUTOR)
# 4. Wong Chi Yan (TP083675)(RECEPTIONIST)


# Symbolic Constants
TUTORS_FILE = "tutors.txt"
RECEPTIONISTS_FILE = "receptionists.txt"
INCOME_FILE = "income.txt"
ADMIN_FILE = "admins.txt"
INCOME_REPORT_FILE = "income_report.txt"
STUDENTS_FILE = "students.txt"
CLASS_INFO_FILE = "classinformation.txt"
ENROLLMENT_FILE = "enrollment.txt"
TUTOR_PROFILE_FILE = "tutor_profile.txt"
PAYMENTS_FILE = "payments.txt"
PENDING_REQUESTS_FILE = "pending_requests.txt"

# Function to load data from a text file


def load_data(filename):
    data = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                row = line.strip().split(',')
                if len(row) >= 2:
                    data.append(row)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# Function to save data to a text file
def save_data(filename, data):
    try:
        with open(filename, "w") as file:
            for row in data:
                row = [str(item) for item in row]
                file.write(",".join(row) + "\n")
        return True
    except Exception as e:
        print(f"Error saving data: {e}")
        return False


# Function to ensure at least one admin account exists
def ensure_admin_exists():
    admins = load_data(ADMIN_FILE)
    admin_exists = any(
        len(admin) >= 3 and admin[2] == "Admin" for admin in admins)
    if not admin_exists:
        print("\nNo admin account found. Creating default admin...")
        default_admin = ["Admin", "AdminPassword1", "Admin"]
        if save_data(ADMIN_FILE, [default_admin]):
            print("Default admin created successfully.")
            print("Username: Admin\nPassword: AdminPassword1\nRole: Admin")
        else:
            print("Failed to create a default admin account.")

# Login and Authentication Functions


def login():
    attempts = 3
    while attempts > 0:
        print("\n=== LOGIN ===")
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()

        # Check credentials against all user types
        user_role = validate_credentials(username, password)

        if user_role:
            print(f"Login successful as {user_role}.")
            return user_role, username
        else:
            attempts -= 1
            print(f"Invalid credentials. {attempts} attempt(s) left.")

    print("Too many failed login attempts. Returning to main menu.")
    return None, None


def validate_credentials(username, password):
    # Check admins first
    admins = load_data(ADMIN_FILE)
    for admin in admins:
        if len(admin) >= 3 and admin[0].lower() == username.lower() and admin[1] == password:
            return "Admin"

    # Check tutors
    tutors = load_data(TUTORS_FILE)
    for tutor in tutors:
        if len(tutor) >= 4 and tutor[0].lower() == username.lower() and tutor[1] == password:
            return "Tutor"

    # Check receptionists
    receptionists = load_data(RECEPTIONISTS_FILE)
    for receptionist in receptionists:
        if len(receptionist) >= 2 and receptionist[0].lower() == username.lower() and receptionist[1] == password:
            return "Receptionist"

    # Check students
    students = load_data(STUDENTS_FILE)
    for student in students:
        if len(student) >= 2 and student[0].lower() == username.lower() and student[1] == password:
            return "Student"

    return None

# Admin Functions


def change_admin_credentials():
    admins = load_data(ADMIN_FILE)
    username = input("Enter current admin username: ").strip()
    password = input("Enter current admin password: ").strip()

    updated = False
    for i in range(len(admins)):
        if len(admins[i]) >= 3 and admins[i][0] == username and admins[i][1] == password and admins[i][2] == "Admin":
            new_username = input("Enter new admin username: ").strip()
            new_password = input("Enter new admin password: ").strip()

            if any(admin[0].lower() == new_username.lower() for admin in admins):
                print("Username already exists. Please choose a different one.")
                return False

            admins[i] = [new_username, new_password, "Admin"]
            updated = True
            break

    if updated and save_data(ADMIN_FILE, admins):
        print("Admin credentials updated successfully.")
        return True
    else:
        print("Failed to update admin credentials.")
        return False


def register_tutor():
    tutors = load_data(TUTORS_FILE)

    while True:
        name = input("Enter tutor username: ").strip()
        if not name:
            print("Username cannot be empty.")
            continue

        if any(tutor[0].lower() == name.lower() for tutor in tutors):
            print("Username already exists. Please choose a different one.")
            continue

        password = input("Enter tutor password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue

        subject = input("Enter subject: ").strip()
        if not subject:
            print("Subject cannot be empty.")
            continue

        level = input("Enter level (Form 1-5): ").strip()
        if level not in [f"Form {i}" for i in range(1, 6)]:
            print("Invalid level. Please enter Form 1-5.")
            continue

        tutors.append([name, password, subject, level])
        if save_data(TUTORS_FILE, tutors):
            print("Tutor registered successfully.")
            break
        else:
            print("Failed to register tutor.")
            break


def delete_tutor():
    tutors = load_data(TUTORS_FILE)
    if not tutors:
        print("No tutors available to delete.")
        return

    print("\nCurrent Tutors:")
    for i, tutor in enumerate(tutors, 1):
        print(f"{i}. {tutor[0]} - {tutor[2]} ({tutor[3]})")

    try:
        choice = int(input("Enter number of tutor to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(tutors):
            tutor = tutors[choice-1]
            confirm = input(
                f"Are you sure you want to delete {tutor[0]}? (Y/N): ").lower()
            if confirm == 'y':
                del tutors[choice-1]
                if save_data(TUTORS_FILE, tutors):
                    print("Tutor deleted successfully.")
                else:
                    print("Failed to delete tutor.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def register_receptionist():
    receptionists = load_data(RECEPTIONISTS_FILE)

    while True:
        name = input("Enter receptionist username: ").strip()
        if not name:
            print("Username cannot be empty.")
            continue

        if any(recep[0].lower() == name.lower() for recep in receptionists):
            print("Username already exists. Please choose a different one.")
            continue

        password = input("Enter receptionist password: ").strip()
        if not password:
            print("Password cannot be empty.")
            continue

        receptionists.append([name, password])
        if save_data(RECEPTIONISTS_FILE, receptionists):
            print("Receptionist registered successfully.")
            break
        else:
            print("Failed to register receptionist.")
            break


def delete_receptionist():
    receptionists = load_data(RECEPTIONISTS_FILE)
    if not receptionists:
        print("No receptionists available to delete.")
        return

    print("\nCurrent Receptionists:")
    for i, receptionist in enumerate(receptionists, 1):
        print(f"{i}. {receptionist[0]}")

    try:
        choice = int(
            input("Enter number of receptionist to delete (0 to cancel): "))
        if choice == 0:
            return
        if 1 <= choice <= len(receptionists):
            receptionist = receptionists[choice-1]
            confirm = input(
                f"Are you sure you want to delete {receptionist[0]}? (y/n): ").lower()
            if confirm == 'y':
                del receptionists[choice-1]
                if save_data(RECEPTIONISTS_FILE, receptionists):
                    print("Receptionist deleted successfully.")
                else:
                    print("Failed to delete receptionist.")
            else:
                print("Deletion cancelled.")
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a valid number.")


def view_income_report():
    income = load_data(PAYMENTS_FILE)
    if not income:
        print("\nNo income records found.")
    else:
        print("\n=== Monthly Income Report ===")
        for record in income:
            print(", ".join(record))


def export_income_report():
    income = load_data(PAYMENTS_FILE)
    if not income:
        print("No income data available to export.")
        return
    report_data = ["=== Brilliant Tuition Centre Income Report ==="]
    report_data.extend([", ".join(record) for record in income])
    report_data.append(
        f"Generated on: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if save_data(INCOME_REPORT_FILE, [line.split(",") for line in report_data]):
        print(f"Income report exported successfully to {INCOME_REPORT_FILE}.")
    else:
        print("Failed to export income report.")

# Admin Menu


def admin_menu():
    while True:
        print("\n=== ADMIN MENU ===")
        print("1. Tutor Management")
        print("2. Receptionist Management")
        print("3. Change Admin Credentials")
        print("4. View Income Report")
        print("5. Export Income Report")
        print("6. Logout")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            while True:
                print("\n=== TUTOR MANAGEMENT ===")
                print("1. Register New Tutor")
                print("2. Delete Tutor")
                print("3. Back to Main Menu")
                sub_choice = input("Enter choice (1-3): ").strip()
                if sub_choice == "1":
                    register_tutor()
                elif sub_choice == "2":
                    delete_tutor()
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "2":
            while True:
                print("\n=== RECEPTIONIST MANAGEMENT ===")
                print("1. Register New Receptionist")
                print("2. Delete Receptionist")
                print("3. Back to Main Menu")
                sub_choice = input("Enter choice (1-3): ").strip()
                if sub_choice == "1":
                    register_receptionist()
                elif sub_choice == "2":
                    delete_receptionist()
                elif sub_choice == "3":
                    break
                else:
                    print("Invalid choice. Please try again.")

        elif choice == "3":
            change_admin_credentials()
        elif choice == "4":
            view_income_report()
        elif choice == "5":
            export_income_report()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1-6.")

# ========================================================================================================
# Receptionist Functions


def register_student():
    students = load_data(STUDENTS_FILE)
    subjects = ["Math", "Science", "English", "History", "Computer"]

    name = input("Name: ").strip()
    password = input("Create student password: ").strip()
    ic = input("IC/Passport: ").strip()
    email = input("Email: ").strip()
    contact = input("Contact: ").strip()
    address = input("Address: ").strip()
    level = input("Level (Form 1 - 5): ").strip()  # subject
    enrol_month = input("Month of Enrollment: ").strip()
    guardian_name = input("Guardian Name: ").strip()
    guardian_contact = input("Guardian Contact: ").strip()
    monthly_fee = float(input("Monthly Fee:RM ").strip())

    print("Available subjects:")
    for i in range(len(subjects)):
        print(f"{i+1}. {subjects[i]}")

    while True:
        selected = input("Pick up to 3 subjects (e.g. 1|3|5): ").split('|')
        if len(selected) > 3:
            print("You can only choose up to 3 subjects.")
            continue
        valid = True
        chosen_subjects = []

        for s in selected:
            s = s.strip()
            if not s.isdigit() or not (1 <= int(s) <= len(subjects)):
                print(
                    f"Invalid option: {s}. Please choose numbers from 1 to {len(subjects)}.")
                valid = False
                break
            else:
                chosen_subjects.append(subjects[int(s) - 1])

        if valid:
            break

    student_data = [
        name, password, ic, email, contact, address,
        level, "|".join(chosen_subjects), enrol_month,
        guardian_name, guardian_contact, str(monthly_fee), "0.00"
    ]

    students.append(student_data)
    if save_data(STUDENTS_FILE, students):
        print("\nStudent registered successfully.")
    else:
        print("\nFailed to register student.")


def accept_payment():
    students = load_data(STUDENTS_FILE)
    payments = load_data(PAYMENTS_FILE)
    ic = input("Enter student IC: ").strip()

    for student in students:
        if student[2] == ic:  # Match student by IC/Passport
            try:
                # Input payment details
                amount = float(input("Enter payment amount: RM "))
                payment_date = input(
                    "Enter payment date (YYYY-MM-DD): ").strip()
                payment_type = input(
                    "Enter payment type (Registration/Monthly/Other): ").strip()

                # Retrieve the student's monthly fee
                monthly_fee = float(student[11]) if student[11].replace(
                    '.', '', 1).isdigit() else 0.0

                if amount > monthly_fee:
                    # Handle overpayment
                    student[11] = "0.00"  # Mark as fully paid
                    overpaid_amount = amount - monthly_fee
                    status = f"Overpaid by RM{overpaid_amount:.2f}"
                    print(f"Overpayment detected. {status}")
                elif amount == monthly_fee:
                    # Fully paid
                    student[11] = "0.00"  # Mark as fully paid
                    status = "Paid"
                    print(f"Payment status: {status}")
                else:
                    # Partial payment
                    remaining_balance = monthly_fee - amount
                    # Update remaining balance
                    student[11] = f"{remaining_balance:.2f}"
                    status = f"Remaining Balance: RM{remaining_balance:.2f}"
                    print(f"Payment status: {status}")

                # Record the payment in the payments file
                new_payment = [ic, f"{amount:.2f}", payment_date, payment_type]
                payments.append(new_payment)

                # Save updated data
                if save_data(STUDENTS_FILE, students) and save_data(PAYMENTS_FILE, payments):
                    print(
                        f"\nPayment of RM{amount:.2f} received from {student[0]}")
                    print(f"Payment status: {status}")
                    print("Payment recorded successfully.")

                    # Generate receipt
                    print("\n=== PAYMENT RECEIPT ===")
                    print(f"Student Name: {student[0]}")
                    print(f"IC: {student[2]}")
                    print(f"Payment Amount: RM{amount:.2f}")
                    print(f"Payment Date: {payment_date}")
                    print(f"Payment Type: {payment_type}")
                    print(f"Payment Status: {status}")
                    print("========================")
                else:
                    print("Payment recorded but failed to save data.")
            except ValueError:
                print("Invalid amount entered. Please enter a valid number.")
            return

    print("Student not found.")


def delete_student():
    students = load_data(STUDENTS_FILE)
    ic = input("Enter student IC to delete: ").strip()

    for i in range(len(students)):
        if students[i][2] == ic:
            confirm = input(
                f"Are you sure you want to delete {students[i][0]}? (y/n): ").lower()
            if confirm == 'y':
                del students[i]  # Delete the student from the list
                if save_data(STUDENTS_FILE, students):  # Save the updated list
                    print("Student deleted successfully.")
                else:
                    print("Failed to delete student.")
                return  # Exit the function after deletion
            else:
                print("Deletion cancelled.")
                return

    print("Student not found.")


def view_students():
    students = load_data(STUDENTS_FILE)
    if not students:
        print("No students registered.")
        return

    print("\n1. View all students")
    print("2. Search for student")
    choice = input("Enter choice (1/2): ").strip()

    if choice == "1":
        print("\n=== ALL STUDENTS ===")
        for student in students:
            print(f"\nName: {student[0]}")
            print(f"IC/Passport: {student[2]}")
            print(f"Level: {student[6]}")
            # Display up to 3 subjects as a single line with "|" separator
            # Limit to the first 3 subjects
            subjects = student[7].split("|")[:3]
            print(f"Subjects: {'|'.join(subjects)}")

    elif choice == "2":
        search_term = input(
            "Enter search term (name/IC/level/subject): ").lower()
        found = False
        for student in students:
            if (search_term in student[0].lower() or
                search_term in student[2].lower() or
                search_term in student[6].lower() or
                    search_term in student[7].lower()):
                print(f"\n=== STUDENT INFO FOR {search_term} ===")
                print(f"Name: {student[0]}")
                print(f"IC/Passport: {student[2]}")
                print(f"Level: {student[6]}")
                print(f"Subjects: {'|'.join(student[7].split('|'))}")
                found = True
        if not found:
            print("No matching students found.")
    else:
        print("Invalid choice.")


def update_profile(current_user):
    receptionists = load_data(RECEPTIONISTS_FILE)
    for i in range(len(receptionists)):
        if receptionists[i][0] == current_user:
            new_username = input("Enter new username: ").strip()
            new_password = input("Enter new password: ").strip()

            # Check if username already exists
            if any(recep[0].lower() == new_username.lower() for recep in receptionists if recep[0] != current_user):
                print("Username already exists. Please choose a different one.")
                return False

            # Update receptionist credentials
            receptionists[i] = [new_username, new_password]
            if save_data(RECEPTIONISTS_FILE, receptionists):
                print("Profile updated successfully.")
                print("You will need to log in again with your new credentials.")
                return
            else:
                print("Failed to update profile.")
            return False

    print("Receptionist not found.")
    return False


def process_subject_change_request():
    # Load pending requests from the file
    pending_requests = load_data(PENDING_REQUESTS_FILE)

    # Check if there are any pending requests
    if not pending_requests:
        print("No pending requests from student found.")
        return

    # Display all pending requests
    print("\n=== PENDING REQUESTS FROM STUDENT ===")
    index = 1
    for request in pending_requests:
        print(f"Request ID: {request[0]}")
        print(f"Username: {request[1]}")
        print(f"Current Subject: {request[2]}")
        print(f"New Subject: {request[3]}")
        print(f"Status: {request[4]}")
        print("-" * 30)
        index += 1

    # Ask the receptionist for the Request ID to process
    request_id = input("\nEnter the Request ID to process: ").strip()

    # Find the request with the matching ID
    for i in range(len(pending_requests)):
        request = pending_requests[i]
        if request[0] == request_id:
            print(f"\nProcessing Request ID: {request_id}")
            print(f"Username: {request[1]}")
            print(f"Current Subject: {request[2]}")
            print(f"New Subject: {request[3]}")

            # Confirm approval or rejection
            action = input(
                "Approve or Reject this request? (approve/reject): ").strip().lower()
            if action == "approve":
                request[4] = "Approved"
                print(f"Request ID {request_id} has been approved.")
            elif action == "reject":
                request[4] = "Rejected"
                print(f"Request ID {request_id} has been rejected.")
            else:
                print("Invalid action. Please enter 'approve' or 'reject'.")
                return

            # Save the updated requests back to the file
            if save_data(PENDING_REQUESTS_FILE, pending_requests):
                print("Request status updated successfully.")
            else:
                print("Failed to update the request status. Please try again.")
            return

    print(f"Error: Request with ID {request_id} does not exist.")

# Receptionist Menu


def receptionist_menu(username):
    while True:

        print(f"\n=== RECEPTIONIST MENU ({username}) ===")
        print("1. Register Student")
        print("2. Update Pending Request From Student")
        print("3. Accept Payment")
        print("4. Delete Student")
        print("5. View Students")
        print("6. Update My Profile")
        print("7. Logout")

        choice = input("Enter your choice (1-7): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            process_subject_change_request()
        elif choice == "3":
            accept_payment()
        elif choice == "4":
            delete_student()
        elif choice == "5":
            view_students()
        elif choice == "6":
            update_profile(username)
            print("Logging out...")
            break
        elif choice == "7":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please enter a number between 1-7.")

# ========================================================================================================
# Tutor Functions


def tutor_menu(username):
    while True:
        print(f"\n=== TUTOR MENU ({username}) ===")
        print("1. Class Information")
        print("2. View Enrolled Students")
        print("3. View My Profile")
        print("4. Update My Profile")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            class_menu(username)
        elif choice == "2":
            view_enrolled_students(username)
        elif choice == "3":
            view_tutor_profile(username)
        elif choice == "4":
            update_tutor_profile(username)
        elif choice == "5":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1-5.")


def class_menu(username):
    while True:
        print(f"\n=== CLASS INFORMATION ({username}) ===")
        print("1. View Class Information")
        print("2. Update Class Information")
        print("3. Delete Class Information")
        print("4. Return to Tutor Menu")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":  # View Class Information
            classes = load_data(CLASS_INFO_FILE)
            found = False

            print("\n=== YOUR CLASSES ===")
            for class_info in classes:
                if len(class_info) > 0 and class_info[0] == username:
                    print(f"1.Subject: {class_info[1]}")
                    print(f"2.Level: {class_info[2]}")
                    print(f"3.Schedule: {class_info[3]}")
                    print(f"4.Charges: RM{class_info[4]}")
                    found = True

            if not found:
                print("No classes assigned to you.")

        elif choice == "2":  # Update Class Information
            classes = load_data(CLASS_INFO_FILE)

            print("\nUpdating class information...")
            for i, class_info in enumerate(classes):
                if len(class_info) > 0 and class_info[0] == username:
                    print(f"1.Subject: {class_info[1]}")
                    print(f"2.Level (form 1 - 5): {class_info[2]}")
                    print(f"3.Schedule: {class_info[3]}")
                    print(f"4.Charges: RM{class_info[4]}")

                    try:
                        field = int(
                            input("Enter field number to update (1-4): "))
                        if 1 <= field <= 4:
                            new_value = input("Enter new value: ").strip()

                            # Basic validation
                            if field == 4 and not new_value.isdigit():
                                print("Charges must be a number.")
                                return class_menu(username)

                            # Correct way to update the field
                            class_info[field] = new_value
                            # Pass the whole classes list
                            if save_data(CLASS_INFO_FILE, classes):
                                print("Class information updated successfully.")
                            else:
                                print("Failed to update class information.")
                        else:
                            print("Invalid field number.")
                    except ValueError:
                        print("Please enter a valid number.")
                    break
                else:
                    print("Class information not found.")

        elif choice == "3":  # Delete Class Information
            classes = load_data(CLASS_INFO_FILE)

            print("\nDeleting class information...")
            try:
                # Ask the tutor to select a class to modify
                class_to_modify = int(
                    input("Enter the number of the class to delete: ")) - 1
                if 0 <= class_to_modify < len(classes) and classes[class_to_modify][0] == username:
                    # Display fields for the selected class
                    print("\n=== Selected Class ===")
                    print(f"1. Subject: {classes[class_to_modify][1]}")
                    print(f"2. Level: {classes[class_to_modify][2]}")
                    print(f"3. Schedule: {classes[class_to_modify][3]}")
                    print(f"4. Charges: RM{classes[class_to_modify][4]}")

                    # Ask which field to clear
                    field_to_clear = int(
                        input("Enter the field number to clear (1-4): "))
                    if 1 <= field_to_clear <= 4:
                        confirm = input(
                            "Are you sure you want to clear this field? (y/n): ").strip().lower()
                        if confirm == "y":
                            # Clear the value
                            classes[class_to_modify][field_to_clear] = ""
                            if save_data(CLASS_INFO_FILE, classes):
                                print("Field cleared successfully.")
                            else:
                                print("Failed to clear the field.")
                        else:
                            print("Clearing cancelled.")
                    else:
                        print("Invalid field number.")
                else:
                    print("Invalid selection.")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "4":
            print("Returning to Tutor Menu...")
            break

        else:
            print("Invalid choice. Please enter a number between 1-4.")


def view_enrolled_students(username):
    enrollments = load_data(ENROLLMENT_FILE)
    students = load_data(STUDENTS_FILE)
    found = False

    print("\n=== YOUR STUDENTS ===")
    for enroll in enrollments:
        if len(enroll) > 0 and enroll[0] == username:
            student_ic = enroll[2]
            for student in students:
                if len(student) > 2 and student[2] == student_ic:
                    print(f"1.Name: {student[0]}")
                    print(f"2.IC: {student[2]}")
                    print(f"3.Level: {student[6]}")
                    print(f"4.Subjects: {student[7]}")
                    found = True
                    break
            break

    if not found:
        print("No students enroled in your classes.")


def view_tutor_profile(username):
    profiles = load_data(TUTOR_PROFILE_FILE)

    for profile in profiles:
        if len(profile) > 0 and profile[0] == username:
            print("\n=== YOUR PROFILE ===")
            print(f"Name: {profile[0]}")
            print(f"Age: {profile[1]}")
            print(f"Email: {profile[2]}")
            print(f"Phone: {profile[3]}")
            print(f"Subject: {profile[4]}")
            print(f"Experience: {profile[5]} years")
            return

        else:
            print("Profile not found.")


def update_tutor_profile(username):
    profiles = load_data(TUTOR_PROFILE_FILE)

    for i, profile in enumerate(profiles):
        if len(profile) > 0 and profile[0] == username:
            print("\n=== Current Profile ===")
            print(f"1. Age: {profile[1]}")
            print(f"2. Email: {profile[2]}")
            print(f"3. Phone: {profile[3]}")
            print(f"4. Subject: {profile[4]}")
            print(f"5. Experience: {profile[5]}")
            print("6. Back to Tutor Menu")

            try:
                field = int(input("Enter field number to update (1-6): "))
                if 1 <= field <= 5:
                    new_value = input("Enter new value: ").strip()

                    # Basic validation
                    if field == 1 and not new_value.isdigit():
                        print("Age must be a number.")

                    elif field == 2 and "@" not in new_value:
                        print("Invalid email format.")

                    elif field == 3 and (not new_value.isdigit() or len(new_value) != 10):
                        print("Phone must be 10 digits.")

                    elif field == 5 and not new_value.isdigit():
                        print("Experience must be a number.")
                        return update_tutor_profile(username)

                    profiles[i][field] = new_value
                    if save_data(TUTOR_PROFILE_FILE, profiles):
                        print("Profile updated successfully.")
                    else:
                        print("Failed to update profile.")
                elif field == 6:
                    print("Returning to Tutor Menu...")
                    return
                else:
                    print("Invalid field number.")
            except ValueError:
                print("Please enter a valid number.")
            return

        else:
            print("Profile not found.")

# ========================================================================================================
# Student Functions


def student_menu(username):
    students = load_data(STUDENTS_FILE)  # Load all students
    student_data = None

    # Find the currently logged-in student's data
    for student in students:
        if student[0].lower() == username.lower():  # Match username
            student_data = student
            break

    if not student_data:
        print("Student data not found. Please contact the administrator.")
        return

    while True:
        print(f"\n=== STUDENT MENU ({username}) ===")
        print("1. View My Schedule")
        print("2. View Payment Status")
        print("3. Update My Profile")
        print("4. Send Request")
        print("5. Delete Pending Request")
        print("6. Logout")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            view_student_schedule(student_data)
        elif choice == "2":
            view_payment_status(student_data)
        elif choice == "3":
            update_student_profile(student_data)
        elif choice == "4":
            send_subject_change_request(username, student_data)
        elif choice == "5":
            delete_request()
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please enter a number between 1-6.")


def view_student_schedule(student_data):
    tutor_classes = load_data(CLASS_INFO_FILE)  # Load all class information
    found = False

    print("\n=== YOUR SCHEDULE ===")
    print(f"Name: {student_data[0]}")
    print(f"Level: {student_data[6]}")
    print("Subjects:")
    for subject in student_data[7].split("|")[:3]:  # Split subjects by "|"
        print(f"- {subject.strip()}")  # Print each subject directly

    # Iterate through the classes to find matching subjects and level
    for class_info in tutor_classes:
        if len(class_info) >= 4:  # Ensure the row has enough fields
            tutor_name, subject, level, time = class_info[:4]
            if subject in student_data[7].split("|") and level == student_data[6]:
                print(f"\nSubject: {subject}")
                print(f"Time: {time}")
                print(f"Teacher: {tutor_name}")
                found = True

    if not found:
        print("No matching schedule found.")


def view_payment_status(student_data):
    balances = load_data(PAYMENTS_FILE)  # Load payment records
    student_ic = student_data[2]  # Get the student's IC/Passport
    total_paid = 0  # Track the total amount paid by the student

    print("\n=== PAYMENT STATUS ===")
    print(f"Name: {student_data[0]}")
    print(f"IC: {student_ic}")

    # Iterate through payment records to find payments for the student
    for balance in balances:
        # Check if the record matches the student's IC
        if len(balance) >= 2 and balance[0] == student_ic:
            print(f"Payment Date: {balance[2]}")
            print(f"Payment Amount: RM{balance[1]}")
            print(f"Payment Type (Registration/Monthly): {balance[3]}")
            # Add the payment amount to the total
            total_paid += float(balance[1])

    # Check if any payments were found
    if total_paid > 0:
        print(f"\nTotal Paid: RM{total_paid}")
    else:
        print("\nNo payments found for this student.")

    # Display outstanding balance if applicable
    if len(student_data) > 11 and student_data[11].isdigit():
        outstanding_balance = float(student_data[11]) - total_paid
        if outstanding_balance > 0:
            print(f"Outstanding Balance: RM{outstanding_balance}")
            print("Please make payment at the reception.")
        else:
            print("Your account is up to date with no balance due.")
    else:
        print("You've payed all your payments.")


def update_student_profile(student_data):
    students = load_data(STUDENTS_FILE)

    for i, student in enumerate(students):
        if len(student) > 0 and student[0] == student_data[0]:
            print("\nCurrent Profile:")
            print(f"1. Email: {student[3]}")
            print(f"2. Contact: {student[4]}")
            print(f"3. Address: {student[5]}")
            print(f"4. Guardian's Name: {student[9]}")
            print(f"5. Guardian's Contact: {student[10]}")

            try:
                field = int(input("Enter field number to update (1-5): "))
                if 1 <= field <= 5:
                    new_value = input("Enter new value: ").strip()

                    # Field 3 is email (index 3 in student list)
                    # Field 4 is contact (index 4)
                    # Field 5 is address (index 5)
                    students[i][field+2] = new_value

                    if save_data(STUDENTS_FILE, students):
                        print("Profile updated successfully.")
                    else:
                        print("Failed to update profile.")
                else:
                    print("Invalid field number.")
            except ValueError:
                print("Please enter a valid number.")
            return

    print("Student record not found.")


def send_subject_change_request(username, student_data):
    # Load existing pending requests
    pending_requests = load_data(PENDING_REQUESTS_FILE)

    # Generate a unique request ID
    request_id = len(pending_requests) + 1

    # Display current subjects
    print("\n=== CURRENT SUBJECTS ===")
    for subject in student_data[7].split("|"):  # Split subjects by "|"
        print(f"- {subject.strip()}")

    # Ask the student for the subject they want to update
    current_subject = input("\nEnter the subject you want to update: ").strip()

    # Validate if the current subject exists in the student's subjects
    if current_subject not in [s.strip() for s in student_data[7].split("|")]:
        print(f"Error: {current_subject} is not in your current subjects.")
        return

    # Ask for the new subject
    print("\nEnter the new subject to replace it:")
    available_subjects = ["Math", "Science", "English", "History", "Computer"]
    for i, subject in enumerate(available_subjects, 1):
        print(f"{i}. {subject}")

    new_subject = input("New subject: ").strip()

    # Validate if the new subject is in the available subjects
    if new_subject not in available_subjects:
        print(f"Error: {new_subject} is not a valid subject.")
        return

    # Create the request as a list
    request = [str(request_id), username, current_subject,
               new_subject, "Pending"]

    # Append the request to the pending requests list
    pending_requests.append(request)

    # Save the updated pending requests back to the file
    if save_data(PENDING_REQUESTS_FILE, pending_requests):
        print(f"\nRequest sent successfully with ID: {request_id}")
        print("Your request is pending approval by the receptionist.")
    else:
        print("Failed to send the request. Please try again.")


def delete_request():
    # Load pending requests from the file
    pending_requests = load_data(PENDING_REQUESTS_FILE)

    # Display all pending requests
    if not pending_requests:
        print("No pending requests found.")
        return

    # Ask the user for the Request ID to delete
    try:
        request_id = input("\nEnter the Request ID to delete: ").strip()

        # Find the request with the matching ID
        for i, request in enumerate(pending_requests):
            # Match Request ID
            if len(request) > 0 and request[0] == request_id:
                confirm = input(
                    f"Are you sure you want to delete Request ID {request_id}? (y/n): ").strip().lower()
                if confirm == "y":
                    del pending_requests[i]  # Delete the request
                    if save_data(PENDING_REQUESTS_FILE, pending_requests):
                        print(
                            f"Request with ID {request_id} deleted successfully.")
                    else:
                        print("Failed to delete the request. Please try again.")
                else:
                    print("Deletion cancelled.")
                return

        print(f"Error: Request with ID {request_id} does not exist.")
    except ValueError:
        print("Invalid Request ID. Please enter a valid number.")

# ========================================================================================================
# Main Program


def main():
    print("\nWelcome to the Brilliant Tuition Centre Management System")
    ensure_admin_exists()

    while True:
        print("\n=== MAIN MENU ===")
        print("1. Login")
        print("2. Exit")
        choice = input("Enter your choice (1 or 2): ").strip()

        if choice == "1":
            role, username = login()
            if role == "Admin":
                admin_menu()
            elif role == "Tutor":
                tutor_menu(username)
            elif role == "Receptionist":
                receptionist_menu(username)
            elif role == "Student":
                student_menu(username)
            else:
                print("Unknown role. Access denied.")
        elif choice == "2":
            print(
                "Thank you for using the Brilliant Tuition Centre Management System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
