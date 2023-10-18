import sys
import re

# Define a dictionary to store status code counts
status_code_counts = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}

total_file_size = 0
line_count = 0

try:
    for line in sys.stdin:
        # Use regular expression to match the expected log line format
        match = re.match(r'(\d+\.\d+\.\d+\.\d+) - \[(.+)\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)', line)
        if match:
            ip, date, status_code, file_size = match.groups()
            # Update total file size
            total_file_size += int(file_size)
            # Update status code counts
            status_code = int(status_code)
            if status_code in status_code_counts:
                status_code_counts[status_code] += 1

            line_count += 1

        # Check if it's time to print statistics
        if line_count >= 10:
            print(f'Total file size: {total_file_size}')
            for code, count in sorted(status_code_counts.items()):
                if count > 0:
                    print(f'{code}: {count}')
            line_count = 0
except KeyboardInterrupt:
    # Handle Ctrl+C by printing the statistics one more time and then exit
    print(f'Total file size: {total_file_size}')
    for code, count in sorted(status_code_counts.items()):
        if count > 0:
            print(f'{code}: {count}')
    sys.exit(0)
