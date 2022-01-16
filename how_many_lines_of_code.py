import os

lines = 0
for file_name in os.listdir():
    if ".py" in file_name:
        with open(file_name) as file:
            number = len(file.readlines())
            print(file_name, number)
            lines += number
print(lines)
