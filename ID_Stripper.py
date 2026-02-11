import os
import glob
for filepath in glob.glob("*.py"):
    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    clean_lines = [line for line in lines if not line.strip().startswith('#') and line.strip() != '']
    with open(filepath, 'w', encoding='utf-8') as file:
        file.writelines(clean_lines)
print("All author comments and personal headers have been stripped!")