import datetime
from select import select

from db_setup import db_connect

class UsersDatabase:
    def __init__(self):
        self.mysql_db = db_connect
        self.db_cursor = self.mysql_db.cursor(buffered=True)

    def create_user(self, email, password):
        self.delete_users()
        exp_date = datetime.date.today() + datetime.timedelta(days = 30)
        self.db_cursor.execute("INSERT INTO users (email, password, date) VALUES (%s, %s, %s)", (email, password, exp_date))
        self.commit()
        return

    def read_user(self, email, password = None, auth=False):
        if auth and password:
            self.db_cursor.execute(f'SELECT password FROM users WHERE email = "{email}"')
            for stored_password in self.db_cursor:
                return (password == stored_password[0])
            raise Exception('Error: Email not found')
        else:
            self.db_cursor.execute(f'SELECT * FROM users WHERE email = "{email}"')
            return dict(zip(self.db_cursor.column_names, self.db_cursor.fetchone()))
            
    def update_user(self, email, password = None, args_dict = None, selected_jobs = None):
        if not args_dict and not selected_jobs:
            self.db_cursor.execute(f"UPDATE users SET password = '{password}' WHERE email = '{email}'")
            self.commit()
        else:
            if args_dict:
                for kwd, value in args_dict.items():
                    try:
                        self.db_cursor.execute(f"UPDATE users SET {kwd} = '{value}' WHERE email = '{email}'")
                        self.commit()
                    except:
                        continue
            elif selected_jobs:
                try:
                    stored_jobs = self.read_user(email=email, auth=False)['pending'].split()
                    for job in stored_jobs:
                        if job not in selected_jobs:
                            selected_jobs.append(job)
                    pending_apps = ' '.join(selected_jobs)
                except:
                    pending_apps = ' '.join(selected_jobs)
                self.db_cursor.execute(f"UPDATE users SET pending = '{pending_apps}' WHERE email = '{email}'")
                self.commit()
        return

    def delete_users(self):
        self.db_cursor.execute(f"DELETE FROM users WHERE date <= CURRENT_DATE();")
        self.commit()
        return

    def commit(self):
        self.mysql_db.commit()