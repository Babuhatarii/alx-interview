#!/usr/bin/python3
import sys
import signal
import re

total_file_size = 0
status_codes_count = {
    "200": 0,
    "301": 0,
    "400": 0,
    "401": 0,
    "403": 0,
    "404": 0,
    "405": 0,
    "500": 0
}
line_count = 0

log_pattern = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<date>.*?)\] "GET /projects/260 HTTP/1.1" (?P<status_code>\d{3}) (?P<file_size>\d+)'
)

def print_statistics():
    """Print the current statistics."""
    print(f"File size: {total_file_size}")
    for code in sorted(status_codes_count.keys()):
        if status_codes_count[code] > 0:
            print(f"{code}: {status_codes_count[code]}")

def signal_handler(sig, frame):
    """Handle the keyboard interrupt signal (CTRL + C)."""
    print_statistics()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

for line in sys.stdin:
    line = line.strip()
    match = log_pattern.match(line)
    if match:
        status_code = match.group('status_code')
        file_size = int(match.group('file_size'))
        
        total_file_size += file_size
        if status_code in status_codes_count:
            status_codes_count[status_code] += 1
        
        line_count += 1
        
        if line_count % 10 == 0:
            print_statistics()

print_statistics()
