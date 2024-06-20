#!/usr/bin/python3
'''Script for parsing logs for HTTP requests.'''
import re


def parse_log_line(line):
    '''Parses a single line of HTTP log and extracts its components.

    Args:
        line (str): A single line from the log file.

    Returns:
        dict: A dictionary containing status_code and file_size.
    '''
    pattern_parts = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"\s*',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)\s*'
    )
    log_pattern = '{}\\-{}{}{}{}'.format(*pattern_parts)
    match = re.fullmatch(log_pattern, line)
    if match:
        return {
            'status_code': match.group('status_code'),
            'file_size': int(match.group('file_size'))
        }
    return {'status_code': 0, 'file_size': 0}


def display_statistics(total_size, status_counts):
    '''Displays the accumulated statistics of the HTTP requests.

    Args:
        total_size (int): The total size of all files.
        status_counts (dict): A dictionary of status codes and their counts.
    '''
    print(f'File size: {total_size}', flush=True)
    for status_code in sorted(status_counts.keys()):
        count = status_counts[status_code]
        if count > 0:
            print(f'{status_code}: {count}', flush=True)


def update_statistics(line, total_size, status_counts):
    '''Updates the total file size and status code counts from a log line.
    '''
    log_info = parse_log_line(line)
    status_code = log_info['status_code']
    if status_code in status_counts:
        status_counts[status_code] += 1
    return total_size + log_info['file_size']


def run():
    '''Runs the log parser.'''
    line_count = 0
    total_file_size = 0
    status_counts = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    try:
        while True:
            line = input()
            total_file_size = update_statistics(line, total_file_size, status_counts)
            line_count += 1
            if line_count % 10 == 0:
                display_statistics(total_file_size, status_counts)
    except (KeyboardInterrupt, EOFError):
        display_statistics(total_file_size, status_counts)


if __name__ == '__main__':
    run()
