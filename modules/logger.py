from datetime import datetime

def __init__(data, filename='log.txt'):
    filename = filename or "log.txt"
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_line = '{} - {}\n'.format(timestamp, data)
    print(data)
    with open(f'./files/{filename}', 'a') as f:
        f.write(log_line)
