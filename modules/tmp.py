from datetime import datetime


def write(data, filename="temp.txt"):
    """

    Writes the given data to a file with the specified filename in the /tmp directory. If filename is not provided, it defaults to 'temp.txt'. The data is also printed to the console. The function appends the data along with a timestamp in the format 'YYYY-MM-DD HH:MM:SS' to the file.

    Args:
        data: The data to be written to the file.
        filename (optional): The name of the file to write the data to. Defaults to 'temp.txt' if not provided.

    Returns:
        None

    """
    filename = filename or "temp.txt"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = "{} - {}\n".format(timestamp, data)
    print(data)
    with open(f"/tmp/{filename}", "a") as f:
        f.write(log_line)
