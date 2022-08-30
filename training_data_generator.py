import tempfile
import json

from database.users_database import UsersDatabase
from storage import StorageManager

class DataGenerator:
    def __init__(self):
        self.users_db = UsersDatabase()
        self.storage_db = StorageManager()

    def create_data(self, email, text):
        entities = []
        replace_values = [['\n', ', '], ['\x01', ' '], ['  ', ' ']]
        for old_val, new_val in replace_values:
            text = text.replace(old_val, new_val)
        allowed_ents = ['fname', 'lname', 'phone', 'degree', 'skills', 'role', 'location']
        user_results = self.users_db.read_user(email = email, auth = False)
        for allowed_ent in allowed_ents:
            if allowed_ent != 'location':
                ent_values = user_results[allowed_ent].split(',')
            set_entities = [entity.strip() if allowed_ent != 'location' else user_results[allowed_ent] for entity in ent_values]
            for entity in set_entities:
                try:
                    ent_index = text.index(entity)
                except:
                    pass
                else:
                    entities.append([ent_index, ent_index + len(entity), allowed_ent])
        if entities != []:
            resume_training_data = json.dumps([text, {"entities": entities}])
            with tempfile.NamedTemporaryFile(dir='./active_files', suffix='.json', mode="w+") as tmp_file:
                json.dump(resume_training_data, tmp_file)
                tmp_file.flush()
                self.storage_db.insert_file(tmp_file)
        return