import os
import time

lines = 0
for file_name in os.listdir():
    if ".py" in file_name and file_name not in []:
        with open(file_name) as file:
            number = len(file.readlines())
            print(file_name, number)
            lines += number
print(lines)
