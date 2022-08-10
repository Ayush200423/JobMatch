import pyrebase
from werkzeug.utils import secure_filename

from storage_config import config

class StorageManager:
    def __init__(self):
        firebase = pyrebase.initialize_app(config)
        self.storage = firebase.storage()

    def insert_resume(self, resume):
        return self.storage.child(f'{secure_filename(resume.filename)}').put(resume)
    
    def get_resume_url(self, filename):
        return self.storage.child(secure_filename(filename)).get_url(None)