import numpy as np
import json
import csv
import os


def login():
    print("\nLogin Required")
    username = input("Username: ")
    password = input("Password: ")
    return username == "admin" and password == "admin123"


class Student:
    def __init__(self, roll_no, name, english, maths, science, present):
        self.roll_no = roll_no
        self.name = name
        self.present = present
        self.marks = {
            "English": english,
            "Maths": maths,
            "Science": science
        }

    def percentage(self):
        if not self.present:
            return 0
        return round(np.mean(list(self.marks.values())), 2)


class EvaluatedStudent(Student):

    def grade(self):
        if not self.present:
            return "Absent"

        avg = self.percentage()

        if avg >= 85:
            return "A"
        elif avg >= 70:
            return "B"
        elif avg >= 50:
            return "C"
        else:
            return "F"

    def status(self):
        if not self.present:
            return "Absent on exam day"

        if any(mark < 35 for mark in self.marks.values()):
            return "Needs Improvement"

        return "Good Performance"


class PerformanceAnalyzer:

    def __init__(self):
        self.students = []
        self.load_records()

    def add_student(self, student):
        self.students.append(student)
        self.save_records()   # ✅ Auto save after adding

   
    def save_records(self, filename="students.json"):
        data = []
        for s in self.students:
            data.append({
                "roll": s.roll_no,
                "name": s.name,
                "marks": s.marks,
                "present": s.present
            })

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_records(self, filename="students.json"):
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        for item in data:
            s = EvaluatedStudent(
                item["roll"],
                item["name"],
                item["marks"]["English"],
                item["marks"]["Maths"],
                item["marks"]["Science"],
                item["present"]
            )
            self.students.append(s)

    def export_report(self, filename="student_report.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            writer.writerow(
                ["Name", "Roll No", "English", "Maths", "Science",
                 "Percentage", "Grade", "Status"]
            )

            for s in self.students:
                writer.writerow([
                    s.name,
                    s.roll_no,
                    s.marks["English"],
                    s.marks["Maths"],
                    s.marks["Science"],
                    s.percentage(),
                    s.grade(),
                    s.status()
                ])

    def show_table(self):
        if not self.students:
            print("No records available.")
            return

        print("\n===== STUDENT PERFORMANCE TABLE =====")
        print("-" * 110)
        print(f"{'Name':15}{'Roll':6}{'Eng':8}{'Math':8}{'Sci':8}"
              f"{'Percent':10}{'Grade':8}{'Status':25}")
        print("-" * 110)

        for s in self.students:
            print(f"{s.name:15}{s.roll_no:<6}"
                  f"{s.marks['English']:<8}"
                  f"{s.marks['Maths']:<8}"
                  f"{s.marks['Science']:<8}"
                  f"{s.percentage():<10}"
                  f"{s.grade():<8}"
                  f"{s.status():<25}")

        print("-" * 110)

def run_program():

    if not login():
        print("Login Failed!")
        return

    analyzer = PerformanceAnalyzer()

    while True:
        print("\n===== MENU =====")
        print("1 Add Student")
        print("2 Show Records")
        print("3 Export Report (Excel CSV)")
        print("4 Exit")

        choice = input("Choice: ")

        if choice == "1":
            try:
                roll = int(input("Roll No: "))
                name = input("Name: ")

                present = input("Present in exam? (y/n): ").lower() == "y"

                if present:
                    english = float(input("English Marks: "))
                    maths = float(input("Maths Marks: "))
                    science = float(input("Science Marks: "))
                else:
                    english = maths = science = 0

                student = EvaluatedStudent(
                    roll, name, english, maths, science, present
                )

                analyzer.add_student(student)  # auto saves
                print("Record added and saved permanently!")

            except ValueError:
                print("Invalid input!")

        elif choice == "2":
            analyzer.show_table()

        elif choice == "3":
            analyzer.export_report()
            print("Report exported as CSV file.")

        elif choice == "4":
            print("Program closed.")
            break

        else:
            print("Invalid choice.")


run_program()
