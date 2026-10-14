import tkinter as tk
from tkinter import ttk, messagebox

# Import data structures, Student class, and file handling from student module
from student import (
    SUBJECTS,
    GRADE_POINTS,
    FILE_NAME,
    score_to_grade,
    Student,
    save_students,
    load_students,
    find_student,
)

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

# GUI class
class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Manager")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG)

        self.students, warning = load_students()   # list of Student objects
        self.score_entries = {}                    # dict: subject -> Entry box
        self.status = tk.StringVar()               # text in the status bar
        self.current_filter = None                 # active grade filter (e.g. "A", "B", etc.)
        self.current_sort = None                   # active sort mode (e.g. "high_to_low", etc.)

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

    def make_menubutton_style(self, style, name, color, hover):
        """Create one colored menubutton style."""
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

        # colored menubuttons (dropdown buttons)
        self.make_menubutton_style(style, "Gold.TMenubutton", GOLD, GOLD_DARK)
        self.make_menubutton_style(style, "Neutral.TMenubutton", GRAY, GRAY_DARK)
        self.make_menubutton_style(style, "Primary.TMenubutton", BLUE, BLUE_DARK)

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
        """Search box, Filter button, and Sort by dropdown button."""
        frame = ttk.LabelFrame(self.root, text="Search & Filter", padding=12)
        frame.pack(fill="x", padx=15, pady=6)

        ttk.Label(frame, text="Name or ID:").pack(side="left", padx=5)
        self.search_entry = ttk.Entry(frame, width=20)
        self.search_entry.pack(side="left", padx=5)
        self.search_entry.bind("<Return>", lambda event: self.search_student())

        ttk.Button(frame, text="Search", style="Primary.TButton",
                   command=self.search_student).pack(side="left", padx=5)
        ttk.Button(frame, text="Show All", style="Neutral.TButton",
                   command=self.show_all).pack(side="left", padx=5)

        # Filter button with dropdown menu
        self.filter_btn = ttk.Menubutton(frame, text="Filter ▾", style="Neutral.TMenubutton")
        filter_menu = tk.Menu(self.filter_btn, tearoff=0, font=("Helvetica", 11),
                              bg=WHITE, fg=TEXT, activebackground=BLUE, activeforeground=WHITE)
        filter_menu.add_command(label="All Grades", command=lambda: self.apply_filter(None, "All"))
        filter_menu.add_separator()
        filter_menu.add_command(label="Grade A  (80-100)", command=lambda: self.apply_filter("A", "Grade A"))
        filter_menu.add_command(label="Grade B+ / B  (70-79)", command=lambda: self.apply_filter("B", "Grade B"))
        filter_menu.add_command(label="Grade C+ / C  (60-69)", command=lambda: self.apply_filter("C", "Grade C"))
        filter_menu.add_command(label="Grade D+ / D  (50-59)", command=lambda: self.apply_filter("D", "Grade D"))
        filter_menu.add_command(label="Grade F  (0-49)", command=lambda: self.apply_filter("F", "Grade F"))
        self.filter_btn.configure(menu=filter_menu)
        self.filter_btn.pack(side="left", padx=5)

        # "Sort by " button containing all requested sort modes
        self.sort_btn = ttk.Menubutton(frame, text="Sort by ▾", style="Gold.TMenubutton")
        sort_menu = tk.Menu(self.sort_btn, tearoff=0, font=("Helvetica", 11),
                            bg=WHITE, fg=TEXT, activebackground=BLUE, activeforeground=WHITE)
        sort_menu.add_command(label="Highest to Lowest",
                              command=lambda: self.apply_sort("high_to_low", "Highest to Lowest"))
        sort_menu.add_command(label="Lowest to Highest",
                              command=lambda: self.apply_sort("low_to_high", "Lowest to Highest"))
        sort_menu.add_separator()
        sort_menu.add_command(label="A - Z",
                              command=lambda: self.apply_sort("a_z", "A - Z"))
        sort_menu.add_command(label="Z - A",
                              command=lambda: self.apply_sort("z_a", "Z - A"))
        sort_menu.add_separator()
        sort_menu.add_command(label="New to Old (Latest Added)",
                              command=lambda: self.apply_sort("new_to_old", "New to Old"))
        sort_menu.add_command(label="Old to New (First Added)",
                              command=lambda: self.apply_sort("old_to_new", "Old to New"))
        sort_menu.add_separator()
        sort_menu.add_command(label="0 to 1 (ID Ascending)",
                              command=lambda: self.apply_sort("0_to_1", "0 to 1"))
        sort_menu.add_command(label="1 to 0 (ID Descending)",
                              command=lambda: self.apply_sort("1_to_0", "1 to 0"))
        self.sort_btn.configure(menu=sort_menu)
        self.sort_btn.pack(side="left", padx=5)

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

    def get_displayed_students(self):
        """Return the list of students according to current search, filter, and sort."""
        result = list(self.students)

        # 1. Search keyword filter
        keyword = self.search_entry.get().strip().lower()
        if keyword != "":
            result = [s for s in result if keyword in s.name.lower() or keyword in s.student_id.lower()]

        # 2. Grade filter
        if self.current_filter is not None:
            result = [s for s in result if s.grade().startswith(self.current_filter)]

        # 3. Sort options
        if self.current_sort == "high_to_low":
            result.sort(key=lambda s: (s.average(), s.gpa()), reverse=True)
        elif self.current_sort == "low_to_high":
            result.sort(key=lambda s: (s.average(), s.gpa()), reverse=False)
        elif self.current_sort == "a_z":
            result.sort(key=lambda s: s.name.upper(), reverse=False)
        elif self.current_sort == "z_a":
            result.sort(key=lambda s: s.name.upper(), reverse=True)
        elif self.current_sort == "new_to_old":
            id_order = {s.student_id: i for i, s in enumerate(self.students)}
            result.sort(key=lambda s: id_order.get(s.student_id, 0), reverse=True)
        elif self.current_sort == "old_to_new":
            id_order = {s.student_id: i for i, s in enumerate(self.students)}
            result.sort(key=lambda s: id_order.get(s.student_id, 0), reverse=False)
        elif self.current_sort == "0_to_1":
            result.sort(key=lambda s: s.student_id, reverse=False)
        elif self.current_sort == "1_to_0":
            result.sort(key=lambda s: s.student_id, reverse=True)

        return result

    def apply_filter(self, grade_letter, label):
        """Filter the table by letter grade."""
        self.current_filter = grade_letter
        if grade_letter is None:
            self.filter_btn.configure(text="Filter ▾")
        else:
            self.filter_btn.configure(text=f"Filter: {label} ▾")

        displayed = self.get_displayed_students()
        self.refresh_table(displayed)

        if grade_letter is None:
            self.status.set(f"Showing all grades ({len(displayed)} student(s)).")
        else:
            self.status.set(f"Filtered by {label} ({len(displayed)} student(s) found).")

    def apply_sort(self, sort_mode, label):
        """Sort the current student table."""
        self.current_sort = sort_mode
        self.sort_btn.configure(text=f"Sort: {label} ▾")

        displayed = self.get_displayed_students()
        self.refresh_table(displayed)
        self.status.set(f"Sorted by {label} ({len(displayed)} student(s)).")

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
        self.refresh_table(self.get_displayed_students())
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
        self.refresh_table(self.get_displayed_students())
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
            self.refresh_table(self.get_displayed_students())
            self.clear_form()
            self.status.set("Deleted " + student.name + ". Total students: " + str(len(self.students)))

    def search_student(self):
        keyword = self.search_entry.get().strip().lower()
        if keyword == "":
            messagebox.showinfo("Search", "Please type a name or ID.")
            return

        displayed = self.get_displayed_students()
        if len(displayed) == 0:
            messagebox.showinfo("Search", "No student found.")
            return

        self.refresh_table(displayed)
        self.status.set("Found " + str(len(displayed)) + " student(s).")

    def show_all(self):
        self.search_entry.delete(0, "end")
        self.current_filter = None
        self.current_sort = None
        self.filter_btn.configure(text="Filter ▾")
        self.sort_btn.configure(text="Sort by ▾")
        self.refresh_table(self.students)
        self.status.set("Showing all " + str(len(self.students)) + " student(s).")

    def show_top_student(self):
        """Show all students sorted from highest to lowest score."""
        self.apply_sort("high_to_low", "Highest to Lowest")

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


# Main program
def main():
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()