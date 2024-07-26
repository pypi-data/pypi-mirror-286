import subprocess
import re
import sys
from auto8.fixers import (
    e501_line_too_long,
    w292_no_newline_at_eof,
    e502_redundant_backslash,
    w291_trailing_whitespace,
    w293_blank_line_whitespace,
    e128_continuation_line_under_indented
)

def run_flake8(file_path=None):
    command = ['flake8']
    if file_path:
        command.append(file_path)
    result = subprocess.run(command, capture_output=True, text=True)
    return result.stdout

def parse_flake8_output(output):
    pattern = r'(.+):(\d+):(\d+): (\w+) (.+)'
    issues = []
    for line in output.split('\n'):
        match = re.match(pattern, line)
        if match:
            file_path, line_num, col_num, error_code, description = match.groups()
            issues.append({
                'file_path': file_path,
                'line_num': int(line_num),
                'col_num': int(col_num),
                'error_code': error_code,
                'description': description
            })
    return issues

def fix_issues(issues):
    fixed_count = 0
    for issue in issues:
        if issue['error_code'] == 'E501':
            e501_line_too_long.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W292':
            w292_no_newline_at_eof.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'E502':
            e502_redundant_backslash.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W291':
            w291_trailing_whitespace.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'W293':
            w293_blank_line_whitespace.fix(issue['file_path'], issue['line_num'])
        elif issue['error_code'] == 'E128':
            e128_continuation_line_under_indented.fix(issue['file_path'], issue['line_num'])
        else:
            continue
        fixed_count += 1
    return fixed_count

def main():
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = None

    max_iterations = 5
    iteration = 0
    total_fixes = 0

    while iteration < max_iterations:
        flake8_output = run_flake8(file_path)
        issues = parse_flake8_output(flake8_output)
        
        if not issues:
            break

        fixes_made = fix_issues(issues)
        total_fixes += fixes_made
        
        if fixes_made == 0:
            break

        iteration += 1

    print(f"Auto8 has completed fixing issues. Total fixes made: {total_fixes}")
    if iteration == max_iterations:
        print("Maximum number of iterations reached. Some issues may remain.")

if __name__ == '__main__':
    main()