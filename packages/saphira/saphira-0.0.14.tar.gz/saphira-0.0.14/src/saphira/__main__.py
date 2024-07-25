import sys

from saphira import *

project = sys.argv[1]
stdin_input = []
tests = {}
curr_test = None
for line in sys.stdin.readlines():
    if '###' in line:
        curr_test = line.strip().split('### ')[1]
        tests[curr_test] = ''
    elif curr_test:
        tests[curr_test] += line.strip() + '\n'
for test_name in tests:
    stdin_input_str = tests[test_name]
    req, s3_link = save_manual_test_input(project, test_name, stdin_input_str)
    if req != 'None':
        update_test_status(project, req, '[FAILING]' not in stdin_input_str, test=s3_link)
    else:
        print('No req matched')