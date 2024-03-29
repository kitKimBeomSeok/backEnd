from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
def read_file_as_string(file_path):
    with open(file_path, 'rb') as file:
        file_content = file.read()
        return file_content