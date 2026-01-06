import tkinter as tk
from datetime import date
from tkinter import font

from habitTable import HabitTable
from wrapper import load_state, save_state

# -------- Main GUI --------
root = tk.Tk()
root.geometry("1200x700")
root.title("Habit Calendar")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
today = date.today()
current_year = today.year
current_month_index = today.month - 1  # 0=Jan


# Label to show clicked cells count
clicked_label = tk.Label(root, text="Clicked cells: 0", font=("Arial", 14))
clicked_label.place(relx=0.5, rely=0.92, anchor="center")

# Store HabitTables
tables = {}

all_data = load_state()


def update_count(count):
    clicked_label.config(text=f"Clicked cells: {count}")


# Create all month tables
def get_or_create_table(year, month_idx):
    # If table already exists, return it
    if (year, month_idx) in tables:
        return tables[(year, month_idx)]

    # Otherwise, create the frame and table
    frame = tk.Frame(root)

    def on_update(count):
        clicked_label.config(text=f"Clicked cells: {count}")
        table_data = {
            "clicked_cells": habit_table.clicked_cells,
            "entries": [e.get() for e in habit_table.entries],
        }
        all_data[(year, month_idx)] = table_data
        save_state(all_data)

    habit_table = HabitTable(
        frame, rows=7, month=month_idx, year=year, on_update=on_update
    )
    tables[(year, month_idx)] = habit_table
    saved_table = all_data.get((year, month_idx))
    if saved_table:
        habit_table.set_clicked_cells(saved_table["clicked_cells"])
        habit_table.set_entries(saved_table["entries"])

    my_font = font.Font(family="Helvetica", size=13, weight="normal")
    clear_btn = tk.Button(
        root, text="Clear All", font=my_font, command=lambda: habit_table.clear_all()
    )
    clear_btn.grid(row=0, column=1, padx=10)

    frame.grid(row=0, column=0)
    frame.lower()

    tables[(year, month_idx)] = habit_table
    return habit_table


# Show a month
def show_month(year, month_idx):
    # Hide all existing tables
    for ht in tables.values():
        ht.frame.lower()

    # Get or create the table for this month
    habit_table = get_or_create_table(year, month_idx)
    habit_table.frame.lift()

    # Update live count label
    clicked_label.config(text=f"Clicked cells: {len(habit_table.clicked_cells)}")


# Navigation buttons
def next_month():
    global current_year_index, current_month_index
    if current_month_index < 11:
        current_month_index += 1
    else:
        if current_month_index == 11:
            current_month_index -= 11
    show_month(current_year, current_month_index)


def prev_month():
    global current_year_index, current_month_index
    if current_month_index > 0:
        current_month_index -= 1
    show_month(current_year, current_month_index)


btn_prev = tk.Button(root, text="Previous Month", command=prev_month)
btn_prev.grid(row=1, column=1)

btn_next = tk.Button(root, text="Next Month", command=next_month)
btn_next.grid(row=1, column=3)
# Show current month at startup
show_month(today.year, today.month - 1)


def on_close():
    for (year, month_idx), table in tables.items():
        all_data[(year, month_idx)] = {
            "clicked_cells": table.clicked_cells,
            "entries": [e.get() for e in table.entries],
        }
    save_state(all_data)
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_close)

root.mainloop()
