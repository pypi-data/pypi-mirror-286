import os

def get_parent_directory(dir):
    return os.path.dirname(dir)

def create_database_dir():
    database_dir = os.path.join(get_parent_directory(get_package_path()), 'database')

    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

def get_package_path():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    return package_dir

def get_database_dir():
    return os.path.join(get_parent_directory(get_package_path()), 'database')

def get_database_path():
    return os.path.join(get_database_dir(), "venv_database.db")

def create_requirement_dir():
    requirement_dir = os.path.join(get_parent_directory(get_package_path()), 'requirements')

    if not os.path.exists(requirement_dir):
        os.makedirs(requirement_dir)

def get_requirement_dir():
    return os.path.join(get_parent_directory(get_package_path()), 'requirements')

def get_requirement_path(venv_id):
    return os.path.joint(get_requirement_dir(), f'{venv_id}.txt')

