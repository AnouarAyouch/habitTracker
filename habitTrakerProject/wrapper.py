import calendar
import json
import os

STATE_FILE = "clicked_cells.json"


def save_state(all_data):
    json_data = {}
    for (year, month), table_data in all_data.items():
        json_data[f"{year}-{month}"] = {
            "clicked_cells": [list(cell) for cell in table_data["clicked_cells"]],
            "entries": table_data["entries"],
        }

    with open("habit_data.json", "w") as f:
        json.dump(json_data, f, indent=4)


def load_state():
    if not os.path.exists("habit_data.json"):
        return {}

    with open("habit_data.json", "r") as f:
        raw = json.load(f)

    data = {}
    for key, table_data in raw.items():
        year, month = map(int, key.split("-"))
        data[(year, month)] = {
            "clicked_cells": {
                tuple(cell) for cell in table_data.get("clicked_cells", [])
            },
            "entries": table_data.get("entries", [""] * 7),  # default empty strings
        }
    return data


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
