import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Check if the specified line is an import statement for 'os'
    if line_num <= len(lines) and re.match(r'^\s*import\s+os\s*$', lines[line_num - 1]):
        # Check if 'os.' is used in the rest of the file
        file_content = ''.join(lines)
        if 'os.' not in file_content:
            # Remove the 'import os' line
            del lines[line_num - 1]
            
            # Remove any blank lines immediately after the removed import
            while line_num <= len(lines) and lines[line_num - 1].strip() == '':
                del lines[line_num - 1]

    with open(file_path, 'w') as file:
        file.writelines(lines)