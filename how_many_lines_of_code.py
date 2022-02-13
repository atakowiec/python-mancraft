import os
import time

lines = 0
for file_name in os.listdir():
    if ".py" in file_name and file_name not in ["how_many_lines_of_code.py"]:
        with open(file_name) as file:
            number = len(file.readlines())
            print(file_name, number)
            lines += number
print(lines)
