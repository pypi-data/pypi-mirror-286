def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num > 2 and line_num <= len(lines):
        # Check for multiple blank lines
        blank_lines = 0
        for i in range(line_num - 2, 0, -1):
            if lines[i].strip() == '':
                blank_lines += 1
            else:
                break

        if blank_lines > 1:
            # Remove excess blank lines, keeping only one
            del lines[line_num - blank_lines:line_num - 1]

    with open(file_path, 'w') as file:
        file.writelines(lines)