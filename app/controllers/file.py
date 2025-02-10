from app.services.file import create_file, file_list

def create_file_controller():
    return create_file()

def file_list_controller():
    return file_list()