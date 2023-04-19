import os
import shutil
import re
import calendar


def rename_files(folder_path):
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            # Extract DAY, MONTH, YEAR from the filename
            match = re.match(
                r"(?P<day>\d{2}) (?P<month>[a-zA-Z]{3}) (?P<year>\d{4})\-gpt.txt", file
            )
            if match:
                day = match.group("day")
                month = match.group("month")
                year = match.group("year")

                # Convert month name to its corresponding number
                month_number = str(list(calendar.month_abbr).index(month)).zfill(2)

                # Construct new filename
                new_filename = f"{year}-{month_number}-{day}.txt"

                # Create a copy of the file with the new name
                old_file_path = os.path.join(folder_path, file)
                new_file_path = os.path.join(folder_path, new_filename)
                shutil.copy(old_file_path, new_file_path)


if __name__ == "__main__":
    folder_path = "/path/to/folder/"
    rename_files(folder_path)
