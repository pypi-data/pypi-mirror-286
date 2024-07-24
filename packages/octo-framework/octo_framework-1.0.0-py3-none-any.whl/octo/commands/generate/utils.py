def read_file(file_path):
    """Reads the content of the file."""
    with open(file_path, "r") as file:
        content = file.readlines()
    return content


def write_file(file_path, content):
    """Writes the content to the file."""
    with open(file_path, "w") as file:
        file.writelines(content)
