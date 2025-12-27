import tkinter as tk


class HabitTable:
    def __init__(self, root, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.buttons = []

        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        weeks = cols // 7
        for w in range(weeks):
            weekLabel = tk.Label(
                root,
                text=f"Week {w + 1}",
                relief="solid",
                bg="lightgreen",
                font=("Arial", 10, "bold"),
            )
            weekLabel.grid(
                row=0, column=1 + w * 7, columnspan=7, sticky="nsew", padx=1, pady=1
            )

        for c in range(cols):
            day_name = days[c % 7]

            labelDay = tk.Label(
                root,
                text=day_name,
                width=4,
                relief="solid",
                bg="lightblue",
            )
            labelDay.grid(row=1, column=c + 1, padx=1, pady=1)

            labelNum = tk.Label(
                root, text=str(c + 1), width=4, relief="solid", bg="lightblue"
            )
            labelNum.grid(row=2, column=c + 1, padx=1, pady=1)

        # HABIT ROWS
        for r in range(rows):
            row_buttons = []

            habitEntry = tk.Entry(
                root,
                width=23,
                relief="solid",
            )
            habitEntry.grid(
                row=r + 3,
                column=0,
                padx=2,
                pady=1,
                sticky="nsew",
            )

            for c in range(cols):
                btn = tk.Button(
                    root,
                    text="",
                    width=3,
                    height=1,
                    relief="solid",
                    bg="white",
                    command=lambda r=r, c=c: self.toggle_cell(r, c),
                )

                btn.grid(row=r + 3, column=c + 1, padx=1, pady=1)

                row_buttons.append(btn)

            self.buttons.append(row_buttons)

        root.grid_columnconfigure(0, weight=2)  # habit column wider
        for c in range(1, cols + 1):
            root.grid_columnconfigure(c, weight=1)

    def toggle_cell(self, row, col):
        btn = self.buttons[row][col]
        if btn["text"] == "✓":
            btn["text"] = ""
            btn["bg"] = "white"
        else:
            btn["text"] = "✓"
            btn["bg"] = "lightgreen"
