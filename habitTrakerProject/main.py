import tkinter as tk
from datetime import date

from habitTable import HabitTable, get_year_months_info

# -------- Main GUI --------
root = tk.Tk()
root.geometry("1200x700")
root.title("5-Year Habit Calendar")

today = date.today()
current_year = today.year
current_month_index = today.month - 1  # 0=Jan

all_years = {y: get_year_months_info(y) for y in range(current_year, current_year + 5)}
year_keys = list(all_years.keys())
current_year_index = 0

# Label to show clicked cells count
clicked_label = tk.Label(root, text="Clicked cells: 0", font=("Arial", 14))
clicked_label.place(relx=0.5, rely=0.92, anchor="center")

# Store HabitTables
tables = {}
clicked_cells_data = {}


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
        clicked_cells_data[(year, month_idx)] = tables[(year, month_idx)].clicked_cells

    habit_table = HabitTable(
        frame, rows=7, month=month_idx, year=year, on_update=on_update
    )

    # Restore previous clicks if they exist
    if (year, month_idx) in clicked_cells_data:
        for r, c in clicked_cells_data[(year, month_idx)]:
            habit_table.toggle_cell(r, c)  # sets button and clicked_cells

    frame.place(relx=0.5, rely=0.5, anchor="center")
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
        if current_year_index < len(year_keys) - 1:
            current_year_index += 1
            current_month_index = 0
    show_month(year_keys[current_year_index], current_month_index)


def prev_month():
    global current_year_index, current_month_index
    if current_month_index > 0:
        current_month_index -= 1
    else:
        if current_year_index > 0:
            current_year_index -= 1
            current_month_index = 11
    show_month(year_keys[current_year_index], current_month_index)


btn_prev = tk.Button(root, text="Previous Month", command=prev_month)
btn_prev.place(relx=0.3, rely=0.95, anchor="center")

btn_next = tk.Button(root, text="Next Month", command=next_month)
btn_next.place(relx=0.7, rely=0.95, anchor="center")

# Show current month at startup
show_month(today.year, today.month - 1)

root.mainloop()
