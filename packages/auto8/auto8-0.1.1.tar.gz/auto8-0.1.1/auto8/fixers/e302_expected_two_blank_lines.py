def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num > 1 and line_num <= len(lines):
        # Check for the end of imports
        for i in range(line_num - 2, 0, -1):
            if not lines[i].strip().startswith(('import', 'from')):
                # Found the last import line
                if line_num - i == 2:  # Only one blank line
                    # Insert an additional blank line
                    lines.insert(i + 1, '\n')
                break

    with open(file_path, 'w') as file:
        file.writelines(lines)