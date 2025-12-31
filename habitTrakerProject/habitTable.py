import calendar
import tkinter as tk
from datetime import date
from tkinter import font


def get_year_months_info(year):
    months = []

    for month in range(1, 13):
        first_weekday, days_in_month = calendar.monthrange(year, month)

        months.append(
            {
                "year": year,
                "month_number": month,
                "month_name": calendar.month_name[month],
                "month_abbr": calendar.month_abbr[month],
                "days_in_month": days_in_month,
                "first_weekday_index": first_weekday,  # 0 = Monday
                "first_weekday_name": calendar.day_name[first_weekday],
                "is_leap_year": calendar.isleap(year),
                "days": [
                    {
                        "day_number": day,
                        "day_name": calendar.day_name[
                            calendar.weekday(year, month, day)
                        ],
                        "day_abbr": calendar.day_abbr[
                            calendar.weekday(year, month, day)
                        ],
                        "weekday_index": calendar.weekday(year, month, day),
                    }
                    for day in range(1, days_in_month + 1)
                ],
            }
        )

    return months


class HabitTable:
    def __init__(self, parent_frame, rows: int, month: int, year: int, on_update=None):
        self.frame = parent_frame
        self.year = year
        self.month = month
        self.on_update = on_update
        year_info = get_year_months_info(self.year)
        month_info = year_info[self.month]
        days = month_info["days"]
        self.rows = rows
        self.cols = month_info["days_in_month"]
        self.buttons = []
        self.clicked_cells = set()
        today = date.today()
        current_day_number = (
            today.day if (today.month - 1 == month and today.year == year) else None
        )
        weeks = self.cols // 7
        tk.Label(
            parent_frame,
            text=f"{month_info['month_name']} {self.year}",
            font=("Arial", 16, "bold"),
            bg="lightyellow",
            width=self.cols + 1,
        ).grid(row=0, column=0, columnspan=self.cols + 1, pady=10)
        for w in range(weeks):
            weekLabel = tk.Label(
                parent_frame,
                text=f"Week {w + 1}",
                relief="solid",
                bg="lightgreen",
                font=("Arial", 10, "bold"),
            )
            weekLabel.grid(
                row=1, column=1 + w * 7, columnspan=7, sticky="nsew", padx=1, pady=1
            )

        for c, day in enumerate(days):
            if day["day_number"] == current_day_number:
                bg_day = "orange"
            else:
                bg_day = "lightblue"
            labelDay = tk.Label(
                parent_frame,
                text=day["day_name"][:3],
                width=4,
                relief="solid",
                bg=bg_day,
            )
            labelDay.grid(row=2, column=c + 1, padx=1, pady=1)

            labelNum = tk.Label(
                parent_frame,
                text=day["day_number"],
                width=3,
                relief="solid",
                bg="lightblue",
            )
            labelNum.grid(row=3, column=c + 1, padx=1, pady=1)
        for r in range(rows):
            row_buttons = []

            my_font = font.Font(family="Helvetica", size=13, weight="normal")
            habitEntry = tk.Entry(parent_frame, width=20, font=my_font)
            habitEntry.grid(
                row=r + 4,
                column=0,
                padx=2,
                pady=1,
                sticky="nsew",
            )

            for c in range(self.cols):
                btn = tk.Button(
                    parent_frame,
                    text="",
                    width=3,
                    height=1,
                    relief="solid",
                    bg="white",
                    command=lambda r=r, c=c: self.toggle_cell(r, c),
                )

                btn.grid(row=r + 4, column=c + 1, padx=1, pady=1)

                row_buttons.append(btn)

            self.buttons.append(row_buttons)

        parent_frame.grid_columnconfigure(0, weight=2)  # habit column wider
        for c in range(1, self.cols + 1):
            parent_frame.grid_columnconfigure(c, weight=1)

    def toggle_cell(self, row, col):
        btn = self.buttons[row][col]

        if (row, col) in self.clicked_cells:
            # uncheck
            btn["text"] = ""
            btn["bg"] = "white"
            self.clicked_cells.remove((row, col))
        else:
            # check
            btn["text"] = "✓"
            btn["bg"] = "lightgreen"
            self.clicked_cells.add((row, col))
        if self.on_update:
            self.on_update(len(self.clicked_cells))
        clicked_buttons = [self.buttons[r][c] for r, c in self.clicked_cells]
