# Student Grade Manager (GUI)

- **Author:** Theeradech Thaopet

- **Student ID:** 6907012660059

- **Course:** Foundation of Computer Programming

- **Built with:** Python 3.15.0 & Tkinter

---

## What is this project?

Student Grade Manager is a desktop application that uses an interface to keep track of student scores in five subjects: Python, Math, Law, English and Finance.

I created Student Grade Manager because calculating grades on paper or with a calculator is very tedious. Students have to add all scores find the average convert each score into a letter grade (A, B+, B, etc.). Then calculate the GPA. This process takes a lot of time. Is easy to produce a math mistake.

With Student Grade Manager you just enter a students ID, name and five test scores. Student Grade Manager automatically calculates the letter grade and GPA and writes all data to a text file called `students.txt` so nothing is lost when the window closes.

---

## Features

Here is what the program can do:

- **Add students:** Provide an ID, name and five scores then click the Add button.

- **Update scores:** Click on a student in the table to load the students information modify scores or name then click Update.

- **Delete students:** Click a student, press Delete. Confirm with Yes/No to avoid accidental deletion.

- **Clear form:** Use one button to clear all input fields.

- **Search:** Find a student by name or ID quickly.

- **Filter by grade:** Use the Filter ▾ button to display students with a chosen letter grade (for example only Grade A or Grade B).

- **Sort by:** Use the Sort by ▾ button to arrange the list in any order:

To lowest score: sort by score from maximum to minimum.

Lowest to highest score: sort by score from minimum to maximum.

A to Z ( by name): sort by name from A to Z.

Z to A (reverse alphabetical): sort by name from Z to A.

New to Old (latest added students first): sort by date added from newest to oldest.

Old to New ( added students first): sort by date added from oldest to newest.

0 To 1 (by ID ascending): sort by ID from smallest to largest.

1 To 0 (by ID descending): sort by ID from largest to smallest.

- **Report card popup:** Double-click a student or click the Report Card button to open a window that looks like a printed report card showing all scores, average and GPA.

- **Color-coded rows:** The table uses colors to show student performance at a glance—green for A blue for B yellow for C orange for D, red for F.

- **Auto-save:** All data is written to `students.txt` whenever a student is added, updated or deleted.

---

## What I. Used from class

- **Variables & basic types:** Use strings for names and IDs integers for test scores and floats for averages and GPA.

- **Lists:** Store the five subjects in a list `["Python" "Math" "Law" "English" "Finance"]`. Use lists to

- **Dictionaries:** Map letter grades to GPA points (`"A": 4.0` `"B+": 3.5` etc.) and assign row colors.

- **. If/else:** Write `score_to_grade()`, with `if-elif-else` to turn numeric scores into letter grades and add functions to save and load files.

- **Classes / OOP:** Create a `Student` class to hold student data (`student_id` `name` `scores`). Provide methods `.average()` `.grade()` `.gpa()` and `.card_text()`.

- **Modules (`import`):** Split the project into separate files so the code stays organized:

`Student.py`: manages the Student class, grades and file saving/loading.

`Grade_manager_gui.py`: manages the Tkinter user interface, buttons and table.

`Main.py`: the file that starts the app.

**File handling:**. Writes `students.txt` line by line using commas to separate values.

**Error handling (`try-except`):** stops the app from crashing if `students.txt` is missing or if letters are entered of numbers in the score boxes.

**Tkinter GUI:** uses labels, entry boxes, buttons, dropdown menubuttons and Treeview tables to build the desktop window.

---

## Project Structure

```text

mini-project/

├── main.py              # Run this file to start the app

├── student.py           # Student class, calculations and file loading/saving

├── grade_manager_gui.py # Tkinter GUI (window, buttons, table)

├── students.txt         # Text file where student data is saved

├── README.md            # Documentation

└──.gitignore           # Ignores __pycache__ folders

```

---

## How to Run

### Requirements

- Python 3 must be installed on your computer.

- Tkinter is already included with Python on Windows and Mac.

*(If you're on Ubuntu or Debian Linux and Tkinter is missing install it with: `sudo apt-get install python3-tk`)*

### Steps to Run

1. Open Terminal on Mac or Linux or Command Prompt / PowerShell on Windows.

2. Navigate to the project folder:

```bash

git pull < url repository>

cd mini-project

```

3. Run the app with: `python main.py` *(or `python3 main.py` on Mac/Linux)*

---

## How to Use It

1. **Adding a student:** enter the Student ID, Name and five scores (0 to 100) then press Add. The student appears in the table.

2. **Editing a student:** click the students row in the table modify the information in the input boxes then press Update.

3. **Deleting a student:** click the student in the table press Delete. Confirm in the popup.

4. **Searching:** type a name or ID in the search box press Enter or click Search. Click Show All to view all students.

5. **Filtering by grade:** click Filter ▾ choose a grade ( Grade A, Grade B) and click All Grades to remove the filter.

6. **Sorting:** click Sort, by ▾. Select the desired order (e.g. Highest score first alphabetical newest added).

7. **Viewing a report card:** click a student, press Report Card (or double‑click the row). A popup shows the report card; click Close when finished.

---

## Grading Scale

| Score | Grade | GPA Points |

| :---: | :---: | :---: |

80 – 100 | **A** | 4.0 |

| 75 – 79 | **B+** | 3.5 |

| 70 – 74 | **B** | 3.0 |

| 65 – 69 | **C+** | 2.5 |

60 – 64 | **C** | 2.0 |

| 55 – 59 | **D+** | 1.5 |

| 50 – 54 | **D** 1.0 |

| 0 – 49 | **F** | 0.0 |

- Average: the sum of five scores divided by five.

- **GPA:** Sum of all grade points divided by five

---

## File Format (students.txt)

Data is saved as text, one student, per line separated by commas:

`StudentID Name,Python,Math,Law,English,Finance`

Example:

```text

6907012660059,THEERADECH THAOPET,78,73,75,70,80

6907012660012,KRERATIKA WICHANGAM,78,69,70,88,67

6907012660032,CHAYAKORN THEPARWUT,89,78,67,76,80

6907012660237,KORSAK KONGPHETSAK,90,65,77,89,79

```