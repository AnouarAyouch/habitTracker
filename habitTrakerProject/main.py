import tkinter as tk

from habitTable import HabitTable

# --- Main Program ---

root = tk.Tk()
root.title("Habit Tracker with Days")

table_frame = tk.Frame(root)
table_frame.pack(padx=50, pady=20)
table = HabitTable(table_frame, rows=7, cols=30)

root.mainloop()
