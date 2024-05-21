import random
import string
import datetime
import os
import shutil

from utilities.config.folder import TEMP_FOLDER, OUTPUT_FOLDER, PERSISTENT_FOLDER

def generate_random_file_name(prefix: str='', extension: str=''):
    if extension: extension = '.'+extension

    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    file_name = f"{prefix}_{current_time}_{random_string}{extension}"
    return file_name

def deploy(item_path: str):
    _, filename = os.path.split(item_path)
    shutil.move(item_path, OUTPUT_FOLDER)
    return os.path.join(OUTPUT_FOLDER, filename)

def load():
    os.makedirs(TEMP_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(PERSISTENT_FOLDER, exist_ok=True)

def clean_folder(folder, delete_folder=False, extension=''):
    if not os.path.exists(folder): return

    file_list = os.listdir(folder)
    for file_name in file_list:
        file_path = os.path.join(folder, file_name)
        if os.path.isfile(file_path) and file_path.endswith(extension):
            os.remove(file_path)
    if delete_folder:
        os.rmdir(folder)
    
def unload():
    clean_folder(TEMP_FOLDER, True)
    clean_folder('.', False, '.mp3')