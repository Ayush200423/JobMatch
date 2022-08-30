import pyrebase
from werkzeug.utils import secure_filename
import os

from storage_config import config

class StorageManager:
    def __init__(self):
        firebase = pyrebase.initialize_app(config)
        self.storage = firebase.storage()

    def insert_file(self, file):
        return self.storage.child(f'{secure_filename(os.path.basename(file.name))}').put(file.name)