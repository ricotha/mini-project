"""
Student Grade Manager
Main Entry Point
Python Mini Project
"""
import tkinter as tk
from grade_manager_gui import StudentApp
import student


def main():
    """Start the Student Grade Manager application."""
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
