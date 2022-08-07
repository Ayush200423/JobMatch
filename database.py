import datetime

from db_setup import db_connect

class Database:
    def __init__(self):
        self.mysql_db = db_connect
        self.db_cursor = self.mysql_db.cursor()

    def add_job(self, country, posting_info):
        url = posting_info['link']
        title = posting_info['title']
        location = posting_info['location']
        company = posting_info['company']
        description = posting_info['description']
        delete_posting_date = datetime.date.today() + datetime.timedelta(days = 7)
        try:
            self.db_cursor.execute(f'INSERT INTO {country}_jobs (date, url, role, location, company, description) VALUES (%s,%s,%s,%s,%s,%s)', (delete_posting_date, url, title, location, company, description))
            self.commit()
            print('Successfully inserted', url)
        except:
            print('Duplicate Listing', url)
        return

    def remove_job(self, country, url):
        self.db_cursor.execute(f'DELETE FROM {country.lower()}_jobs WHERE url="{url}"')
        self.commit()

    def get_job(self, country, role = None, region = None, date = False, url = None):
        results = []
        if role != None and region != None:
            self.db_cursor.execute(f'SELECT url FROM {country.lower()}_jobs WHERE role LIKE "{role}" AND location LIKE "{region}"')
            for url in self.db_cursor:
                results.append(url)
        elif url != None:
            self.db_cursor.execute(f'SELECT * FROM {country.lower()}_jobs WHERE url = "{url}"')
            for job in self.db_cursor:
                results = {
                    'date added': job[0] - datetime.timedelta(days = 7),
                    'link': job[1],
                    'title': job[2],
                    'location': job[3],
                    'company': job[4],
                    'description': job[5]
                }
        elif date == True:
            self.db_cursor.execute(f'SELECT url FROM {country.lower()}_jobs WHERE date <= CURRENT_DATE();')
            for url in self.db_cursor:
                results.append(url)
        return results

    def commit(self):
        self.mysql_db.commit()