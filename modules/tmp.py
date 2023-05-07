from datetime import datetime

def write(data, filename='temp.txt'):
    filename = filename or "temp.txt"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = '{} - {}\n'.format(timestamp, data)
    print(data)
    with open(f'/tmp/{filename}', 'a') as f:
        f.write(log_line)
