def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        content = file.read()
    
    if not content.endswith('\n'):
        with open(file_path, 'a') as file:
            file.write('\n')