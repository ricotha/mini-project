"""
Student Module
Contains Student class, grading functions, and file handling.
Python Mini Project
"""

# Data structures
SUBJECTS = ["Python", "Math", "Law", "English", "Finance"]  # list

GRADE_POINTS = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5,
                "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}    # dict

FILE_NAME = "students.txt"


# Function: score -> grade
def score_to_grade(score):
    """Convert a score (0-100) to a letter grade."""
    if score >= 80:
        return "A"
    elif score >= 75:
        return "B+"
    elif score >= 70:
        return "B"
    elif score >= 65:
        return "C+"
    elif score >= 60:
        return "C"
    elif score >= 55:
        return "D+"
    elif score >= 50:
        return "D"
    else:
        return "F"


# Object-Oriented Programming: Student class
class Student:
    def __init__(self, student_id, name, scores):
        self.student_id = student_id   # text, e.g. "6907012660059"
        self.name = name               # text, e.g. "RICO"
        self.scores = scores           # list of 5 numbers

    def average(self):
        """Average of all scores."""
        return sum(self.scores) / len(self.scores)

    def grade(self):
        """Letter grade from the average."""
        return score_to_grade(self.average())

    def gpa(self):
        """GPA = average of grade points (all subjects have equal credit)."""
        total = 0
        for score in self.scores:
            total += GRADE_POINTS[score_to_grade(score)]
        return total / len(self.scores)

    def card_text(self):
        """Return the report card as text (shown in a popup window)."""
        border = "+" + "-" * 30 + "+"
        divider = "|" + "-" * 30 + "|"
        lines = [border,
                 "|" + "REPORT CARD".center(30) + "|",
                 divider,
                 "| Name : " + self.name.ljust(22)[:22] + "|",
                 "| ID   : " + self.student_id.ljust(22)[:22] + "|",
                 divider]
        for i in range(len(SUBJECTS)):
            text = f" {SUBJECTS[i]:<12}{self.scores[i]:>5}{score_to_grade(self.scores[i]):>8}"
            lines.append("|" + text.ljust(30) + "|")
        lines.append(divider)
        lines.append("|" + f" Average : {self.average():.2f}".ljust(30) + "|")
        lines.append("|" + f" GPA     : {self.gpa():.2f}".ljust(30) + "|")
        lines.append("|" + f" Result  : {self.grade()}".ljust(30) + "|")
        lines.append(border)
        return "\n".join(lines)

    def to_line(self):
        """Make one line of text to save in the file."""
        text = self.student_id + "," + self.name
        for score in self.scores:
            text = text + "," + str(score)
        return text


# File handling
def save_students(students, filename=FILE_NAME):
    """Write all students to the file (one student per line)."""
    with open(filename, "w") as file:
        for student in students:
            file.write(student.to_line() + "\n")


def load_students(filename=FILE_NAME):
    """Read students from the file.
    Return (list of Student, warning text). Warning is "" if all is fine."""
    students = []
    warning = ""
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split(",")          # ["001", "RICO", "88", ...]
                scores = []
                for text in parts[2:]:
                    scores.append(int(text))
                students.append(Student(parts[0], parts[1], scores))
    except FileNotFoundError:
        warning = ""                              # first run: no file yet, this is OK
    except ValueError:
        warning = "The file has wrong data. Some students were not loaded."
    return students, warning


def find_student(students, student_id):
    """Return the Student with this ID, or None if not found."""
    for student in students:
        if student.student_id == student_id:
            return student
    return None
