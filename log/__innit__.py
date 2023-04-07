import datetime

def log(text, filename='log.txt'):
    now = datetime.datetime.now()
    timestamp = now.strftime('%Y-%m-%d %H:%M:%S')
    log_line = f'{timestamp} - {text}\n'
    with open('./log/' +filename, 'a') as f:
        f.write(log_line)
        
log('hello', 'wtf')