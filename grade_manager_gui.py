"""
Student Grade Manager (Tkinter GUI Version)
Python Mini Project
"""

import tkinter as tk
from tkinter import ttk, messagebox

# =====================================================
# Data structures
# =====================================================
SUBJECTS = ["Python", "Math", "Law", "English", "Finance"]  # list

GRADE_POINTS = {"A": 4.0, "B+": 3.5, "B": 3.0, "C+": 2.5,
                "C": 2.0, "D+": 1.5, "D": 1.0, "F": 0.0}    # dict

FILE_NAME = "students.txt"

# =====================================================
# Color theme (professional style: navy + blue + soft colors)
# =====================================================
NAVY = "#1F3A5F"        # banner, table heading
BLUE = "#2E6DA4"        # main buttons
BLUE_DARK = "#245889"
GREEN = "#2E8B57"       # update button
GREEN_DARK = "#256F46"
RED = "#B03A48"         # delete button
RED_DARK = "#8F2E3A"
GRAY = "#6C757D"        # neutral buttons
GRAY_DARK = "#565E64"
GOLD = "#B7791F"        # top student button
GOLD_DARK = "#946118"
BG = "#F4F6F9"          # window background
WHITE = "#FFFFFF"
TEXT = "#1F2933"        # normal text
LIGHT_TEXT = "#C9D6E8"  # small text on the navy banner

# soft row colors in the table (one color for each grade letter)
GRADE_COLORS = {"A": "#E3F4E8",   # light green
                "B": "#E6F0FA",   # light blue
                "C": "#FFF4DB",   # light amber
                "D": "#FBE9E0",   # light orange
                "F": "#FBE4E4"}   # light red


# =====================================================
# Function: score -> grade
# =====================================================
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


# =====================================================
# Object-Oriented Programming: Student class
# =====================================================
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


# =====================================================
# File handling
# =====================================================
def save_students(students):
    """Write all students to the file (one student per line)."""
    with open(FILE_NAME, "w") as file:
        for student in students:
            file.write(student.to_line() + "\n")


def load_students():
    """Read students from the file.
    Return (list of Student, warning text). Warning is "" if all is fine."""
    students = []
    warning = ""
    try:
        with open(FILE_NAME, "r") as file:
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


# =====================================================
# GUI class
# =====================================================
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Manager")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG)

        self.students, warning = load_students()   # list of Student objects
        self.score_entries = {}                    # dict: subject -> Entry box
        self.status = tk.StringVar()               # text in the status bar

        self.setup_styles()
        self.build_banner()
        self.build_form()
        self.build_search_bar()
        self.build_status_bar()
        self.build_table()

        self.refresh_table(self.students)
        self.status.set("Loaded " + str(len(self.students)) + " student(s).")
        if warning != "":
            messagebox.showwarning("Warning", warning)

    # ---------- Colors and styles ----------
    def make_button_style(self, style, name, color, hover):
        """Create one colored button style."""
        style.configure(name, background=color, foreground=WHITE,
                        font=("Helvetica", 11, "bold"), padding=(14, 6),
                        borderwidth=0, focusthickness=0)
        style.map(name, background=[("active", hover), ("pressed", hover)],
                  foreground=[("active", WHITE)])

    def setup_styles(self):
        """Set the colors and fonts of all widgets."""
        style = ttk.Style()
        style.theme_use("clam")   # this theme allows custom colors on every system

        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Helvetica", 11))
        style.configure("TLabelframe", background=BG, bordercolor="#C5CEDA")
        style.configure("TLabelframe.Label", background=BG, foreground=NAVY,
                        font=("Helvetica", 12, "bold"))
        style.configure("TEntry", padding=4, fieldbackground=WHITE)

        # table
        style.configure("Treeview", background=WHITE, fieldbackground=WHITE,
                        foreground=TEXT, rowheight=28, font=("Helvetica", 11),
                        bordercolor="#C5CEDA")
        style.configure("Treeview.Heading", background=NAVY, foreground=WHITE,
                        font=("Helvetica", 11, "bold"), padding=6, relief="flat")
        style.map("Treeview.Heading", background=[("active", BLUE)])
        style.map("Treeview", background=[("selected", BLUE)],
                  foreground=[("selected", WHITE)])

        # colored buttons
        self.make_button_style(style, "Primary.TButton", BLUE, BLUE_DARK)
        self.make_button_style(style, "Success.TButton", GREEN, GREEN_DARK)
        self.make_button_style(style, "Danger.TButton", RED, RED_DARK)
        self.make_button_style(style, "Neutral.TButton", GRAY, GRAY_DARK)
        self.make_button_style(style, "Gold.TButton", GOLD, GOLD_DARK)
        self.make_button_style(style, "Navy.TButton", NAVY, BLUE_DARK)

    # ---------- Build the window ----------
    def build_banner(self):
        """Top banner with the title."""
        banner = tk.Frame(self.root, bg=NAVY)
        banner.pack(fill="x")
        tk.Label(banner, text="Student Grade Manager", bg=NAVY, fg=WHITE,
                 font=("Helvetica", 20, "bold")).pack(anchor="w", padx=20, pady=(14, 0))
        tk.Label(banner, text="Score management and report card system", bg=NAVY,
                 fg=LIGHT_TEXT, font=("Helvetica", 11)).pack(anchor="w", padx=20, pady=(0, 12))
        tk.Frame(self.root, bg=GOLD, height=3).pack(fill="x")   # thin gold line

    def build_form(self):
        """Form part: Entry boxes and the Add/Update/Delete/Clear buttons."""
        frame = ttk.LabelFrame(self.root, text="Student Information", padding=12)
        frame.pack(fill="x", padx=15, pady=(12, 6))

        ttk.Label(frame, text="Student ID:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.id_entry = ttk.Entry(frame, width=20)
        self.id_entry.grid(row=0, column=1, columnspan=2, sticky="w", padx=5, pady=5)

        ttk.Label(frame, text="Name:").grid(row=0, column=3, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(frame, width=25)
        self.name_entry.grid(row=0, column=4, columnspan=3, sticky="w", padx=5, pady=5)

        # one Label + Entry for every subject (loop over the SUBJECTS list)
        column = 0
        for subject in SUBJECTS:
            ttk.Label(frame, text=subject + ":").grid(row=1, column=column, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame, width=8)
            entry.grid(row=1, column=column + 1, sticky="w", padx=5, pady=5)
            self.score_entries[subject] = entry
            column += 2

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=2, column=0, columnspan=10, sticky="w", pady=(10, 0))
        ttk.Button(button_frame, text="Add", style="Primary.TButton",
                   command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update", style="Success.TButton",
                   command=self.update_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete", style="Danger.TButton",
                   command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", style="Neutral.TButton",
                   command=self.clear_form).pack(side="left", padx=5)

    def build_search_bar(self):
        """Search box and buttons."""
        frame = ttk.LabelFrame(self.root, text="Search", padding=12)
        frame.pack(fill="x", padx=15, pady=6)

        ttk.Label(frame, text="Name or ID:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(frame, width=25)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_student())

        ttk.Button(frame, text="Search", style="Primary.TButton",
                   command=self.search_student).pack(side="left", padx=5)
        ttk.Button(frame, text="Show All", style="Neutral.TButton",
                   command=self.show_all).pack(side="left", padx=5)
        ttk.Button(frame, text="Top Student", style="Gold.TButton",
                   command=self.show_top_student).pack(side="left", padx=5)
        ttk.Button(frame, text="Report Card", style="Navy.TButton",
                   command=self.show_card).pack(side="left", padx=5)

    def build_status_bar(self):
        """Bottom bar that shows messages."""
        bar = tk.Label(self.root, textvariable=self.status, bg="#E1E7EF", fg=NAVY,
                       font=("Helvetica", 11), anchor="w", padx=15, pady=6)
        bar.pack(fill="x", side="bottom")

    def build_table(self):
        """The table (Treeview) that lists all students, with a color legend."""
        # color legend at the bottom of the table area
        legend = ttk.Frame(self.root)
        legend.pack(fill="x", side="bottom", padx=15, pady=(0, 8))
        ttk.Label(legend, text="Row colors:").pack(side="left", padx=(0, 6))
        legend_items = [("A", "A  (80-100)"), ("B", "B+ / B  (70-79)"),
                        ("C", "C+ / C  (60-69)"), ("D", "D+ / D  (50-59)"),
                        ("F", "F  (0-49)")]
        for letter, text in legend_items:
            tk.Label(legend, text=text, bg=GRADE_COLORS[letter], fg=TEXT,
                     font=("Helvetica", 10), padx=8, pady=2).pack(side="left", padx=3)

        frame = ttk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=15, pady=6)

        columns = ["ID", "Name"] + SUBJECTS + ["Average", "GPA", "Grade"]
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
        for name in columns:
            self.tree.heading(name, text=name)
            if name == "ID":
                self.tree.column(name, width=140, anchor="center")
            elif name == "Name":
                self.tree.column(name, width=140, anchor="center")
            else:
                self.tree.column(name, width=80, anchor="center")

        # one row color for each grade letter
        for letter in GRADE_COLORS:
            self.tree.tag_configure(letter, background=GRADE_COLORS[letter])

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)   # click a row
        self.tree.bind("<Double-1>", self.show_card)           # double-click a row

    # ---------- Helper methods ----------
    def refresh_table(self, student_list):
        """Clear the table, then show the students in student_list."""
        self.tree.delete(*self.tree.get_children())
        for student in student_list:
            values = [student.student_id, student.name] + student.scores
            values.append(f"{student.average():.2f}")
            values.append(f"{student.gpa():.2f}")
            values.append(student.grade())
            letter = student.grade()[0]     # "B+" -> "B", used to pick the row color
            # iid = student ID, so we can find the student again when a row is clicked
            self.tree.insert("", "end", iid=student.student_id, values=values, tags=(letter,))

    def clear_form(self):
        """Empty all Entry boxes."""
        self.id_entry.delete(0, "end")
        self.name_entry.delete(0, "end")
        for subject in SUBJECTS:
            self.score_entries[subject].delete(0, "end")
        self.tree.selection_remove(self.tree.selection())

    def read_form(self):
        """Read and check the Entry boxes.
        Return (id, name, scores) or None if something is wrong."""
        student_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip().upper().replace(",", " ")

        if student_id == "":
            messagebox.showerror("Error", "Student ID cannot be empty.")
            return None
        if "," in student_id:
            messagebox.showerror("Error", "Student ID cannot contain a comma.")
            return None
        if name == "":
            messagebox.showerror("Error", "Name cannot be empty.")
            return None

        scores = []
        for subject in SUBJECTS:
            text = self.score_entries[subject].get().strip()
            try:
                score = int(text)
            except ValueError:
                messagebox.showerror("Error", subject + " score must be a number.")
                return None
            if score < 0 or score > 100:
                messagebox.showerror("Error", subject + " score must be between 0 and 100.")
                return None
            scores.append(score)

        return student_id, name, scores

    # ---------- Button actions ----------
    def on_select(self, event=None):
        """When a row is clicked, copy that student into the Entry boxes."""
        selected = self.tree.selection()
        if len(selected) == 0:
            return
        student = find_student(self.students, selected[0])
        if student is None:
            return

        self.id_entry.delete(0, "end")
        self.id_entry.insert(0, student.student_id)
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, student.name)
        for i in range(len(SUBJECTS)):
            entry = self.score_entries[SUBJECTS[i]]
            entry.delete(0, "end")
            entry.insert(0, str(student.scores[i]))

    def add_student(self):
        data = self.read_form()
        if data is None:
            return
        student_id, name, scores = data

        if find_student(self.students, student_id) is not None:
            messagebox.showerror("Error", "This ID already exists.")
            return

        self.students.append(Student(student_id, name, scores))
        save_students(self.students)
        self.refresh_table(self.students)
        self.clear_form()
        self.status.set("Added " + name + ". Total students: " + str(len(self.students)))

    def update_student(self):
        data = self.read_form()
        if data is None:
            return
        student_id, name, scores = data

        student = find_student(self.students, student_id)
        if student is None:
            messagebox.showerror(
                "Error", "Student not found.\nClick a student in the table first (the ID cannot be changed).")
            return

        student.name = name
        student.scores = scores
        save_students(self.students)
        self.refresh_table(self.students)
        self.clear_form()
        self.status.set("Updated " + name + ".")

    def delete_student(self):
        student_id = self.id_entry.get().strip()
        student = find_student(self.students, student_id)
        if student is None:
            messagebox.showerror("Error", "Student not found.\nClick a student in the table first.")
            return

        if messagebox.askyesno("Delete", "Delete " + student.name + "?"):
            self.students.remove(student)
            save_students(self.students)
            self.refresh_table(self.students)
            self.clear_form()
            self.status.set("Deleted " + student.name + ". Total students: " + str(len(self.students)))

    def search_student(self):
        keyword = self.search_entry.get().strip().lower()
        if keyword == "":
            messagebox.showinfo("Search", "Please type a name or ID.")
            return

        result = []
        for student in self.students:
            if keyword in student.name.lower() or keyword in student.student_id.lower():
                result.append(student)

        if len(result) == 0:
            messagebox.showinfo("Search", "No student found.")
            return

        self.refresh_table(result)
        self.status.set("Found " + str(len(result)) + " student(s).")

    def show_all(self):
        self.search_entry.delete(0, "end")
        self.refresh_table(self.students)
        self.status.set("Showing all " + str(len(self.students)) + " student(s).")

    def show_top_student(self):
        if len(self.students) == 0:
            messagebox.showinfo("Top Student", "No students yet.")
            return

        best = self.students[0]
        for student in self.students:
            if student.average() > best.average():
                best = student

        self.refresh_table([best])
        self.status.set("Top student: " + best.name + " (average " + f"{best.average():.2f}" + ")")

    def show_card(self, event=None):
        """Open a popup window with the report card of the selected student."""
        selected = self.tree.selection()
        if len(selected) == 0:
            messagebox.showinfo("Report Card", "Please click a student in the table first.")
            return
        student = find_student(self.students, selected[0])
        if student is None:
            return

        popup = tk.Toplevel(self.root)
        popup.title("Report Card")
        popup.configure(bg=BG)
        tk.Label(popup, text="Student Report Card", bg=NAVY, fg=WHITE,
                 font=("Helvetica", 14, "bold"), pady=10).pack(fill="x")
        tk.Label(popup, text=student.card_text(), font=("Courier", 14),
                 bg=WHITE, fg=NAVY, justify="left", padx=20, pady=20).pack(padx=20, pady=15)
        ttk.Button(popup, text="Close", style="Primary.TButton",
                   command=popup.destroy).pack(pady=(0, 15))


# =====================================================
# Main program
# =====================================================
def main():
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()


main()