import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num <= len(lines):
        # Remove trailing whitespace
        line = lines[line_num - 1]
        
        # Handle the special case of whitespace after "),":
        line = re.sub(r'\),\s+$', '),\n', line)
        
        # Remove any remaining trailing whitespace
        line = line.rstrip() + '\n'
        
        lines[line_num - 1] = line

    with open(file_path, 'w') as file:
        file.writelines(lines)