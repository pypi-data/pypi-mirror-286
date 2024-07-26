# auto8/auto8/fixers/e501_line_too_long.py

import re

def fix(file_path, line_num):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if line_num <= len(lines):
        original_line = lines[line_num - 1].rstrip('\n')
        indent = len(original_line) - len(original_line.lstrip())
        
        # Check if the line starts with a function call or assignment
        match = re.match(r'^(\s*)(\w+\s*=\s*)?(\w+\()(.*)(\))$', original_line)
        if match:
            prefix = match.group(1) + (match.group(2) or '') + match.group(3)
            content = match.group(4)
            suffix = match.group(5)
            
            # Split the content
            if content.startswith('"') or content.startswith("'"):
                quote = content[0]
                string_content = content[1:-1]  # Remove quotes
                words = string_content.split()
                new_lines = [prefix]
                current_line = ' ' * (indent + 4) + quote  # 4 spaces for continuation indent
                
                for word in words:
                    if len(current_line) + len(word) + 1 <= 79 - len(quote) - len(suffix):
                        current_line += word + ' '
                    else:
                        new_lines.append(current_line.rstrip() + ' \\')
                        current_line = ' ' * (indent + 4) + word + ' '
                
                new_lines.append(current_line.rstrip() + quote + suffix)
            else:
                # Handle non-string content
                words = content.split()
                new_lines = [prefix]
                current_line = ' ' * (indent + 4)
                
                for word in words:
                    if len(current_line) + len(word) + 1 <= 79 - len(suffix):
                        current_line += word + ' '
                    else:
                        new_lines.append(current_line.rstrip())
                        current_line = ' ' * (indent + 4) + word + ' '
                
                new_lines.append(current_line.rstrip() + suffix)
            
            lines[line_num - 1] = '\n'.join(new_lines) + '\n'
        else:
            # Handle lines that are not function calls or assignments
            words = original_line.split()
            new_lines = []
            current_line = ' ' * indent

            for word in words:
                if len(current_line) + len(word) + 1 <= 79:
                    current_line += word + ' '
                else:
                    new_lines.append(current_line.rstrip())
                    current_line = ' ' * indent + word + ' '
            
            new_lines.append(current_line.rstrip())
            lines[line_num - 1] = '\n'.join(new_lines) + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)