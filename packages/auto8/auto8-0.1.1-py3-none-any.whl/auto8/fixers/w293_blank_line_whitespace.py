def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num <= len(lines):
        # Check if the line is blank (only whitespace)
        if lines[line_num - 1].strip() == '':
            # Replace the line with a single newline character
            lines[line_num - 1] = '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)