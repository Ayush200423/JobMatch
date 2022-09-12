from bs4 import BeautifulSoup
import asyncio
import aiohttp
import requests
from concurrent.futures import ThreadPoolExecutor

from format_location import CorrectFormatting
from database.jobs_database import JobsDatabase

class Scraper:
    def __init__(self, country, role = 'All'):
        locale_codes = {'USA': 'com', 'CANADA': 'ca'}
        self.role = role
        self.country = country
        self.country_code = locale_codes[self.country]
        self.url = f'https://www.careerjet.{self.country_code}'
        self.jobs = []
        self.requests_session = requests.Session()
        self.get_url()

    def get_url(self):
        self.query_params = '/search/jobs?'
        if self.role != 'All':
            self.role = self.role.replace(' ', '+')
            self.query_params += f's={self.role}'
        self.country = self.country.replace(' ', '+').replace(',', '%2C')
        self.query_params += f'&l={self.country}'

    def get_posting_links(self, page):
        posting_links = []
        link = f'{self.url}{self.query_params}&p={page}&ay=1&sort=date'
        page = self.requests_session.get(link)
        doc = BeautifulSoup(page.text, 'lxml')
        try:
            doc.find('pre').text
        except:
            divs = doc.find_all('article', {'class' : 'job clicky'})
            for posting in divs:
                title_tag = posting.find('h2')
                posting_links.append(self.url + title_tag.find('a')['href'])
        else:
            pass
        return posting_links

    def get_details(self, data):
        for posting in data:
            description = []
            posting_doc = BeautifulSoup(posting[1], 'lxml')
            entire_page = posting_doc.find('div', {'class' : 'container'})
            title_company_location = entire_page.find('header')
            location = self.clean_text(title_company_location.find('ul', {'class', 'details'}).find('span').text, [['\n', '']])
            description_section = entire_page.find('section', {'class' : 'content'})
            description_ul = description_section.find_all('li')
            for line in description_ul:
                description.append(self.clean_text((line.text), [['"', ''], ["'", ''], ['\n', ''], ['.', ','], ['/', ' ']]).rstrip(','))
            if description != []:
                try:
                    self.details = {
                        'link': posting[0],
                        'title': self.clean_text(title_company_location.find('h1').text, [['\n', '']]),
                        'location': CorrectFormatting(self.country, location = location).format(),
                        'company': self.clean_text(title_company_location.find('p', {'class' : 'company'}).text, [["'", ''], ['\n', '']]),
                        'description': ", ".join(description)
                    }
                    self.jobs.append(self.details)
                except AttributeError:
                    self.jobs.append('Error')
            else:
                self.jobs.append('Error')
        return self.jobs
    
    def clean_text(self, text, to_replace):
        for val in to_replace:
            text = text.replace(val[0], val[1]).strip()
        return text

    async def get_page(self, link, session):
        async with session.get(link) as posting_page:
            html = await posting_page.text()
            return [link, html]

    async def get_tasks(self, posting_links, session):
        tasks = []
        for link in posting_links:
            task = asyncio.create_task(self.get_page(link, session))
            tasks.append(task)
        results = await asyncio.gather(*tasks)
        return results
    
    async def get_data(self, posting_links):
        async with aiohttp.ClientSession() as session:
            data = await self.get_tasks(posting_links, session)
            return data

    def get_jobs(self, max_pages):
        with ThreadPoolExecutor() as executor:
            posting_links = list(executor.map(self.get_posting_links, range(1, max_pages + 1)))
            flattened_links_list = [link for page in posting_links for link in page]
            data = asyncio.run(self.get_data(flattened_links_list))
            self.get_details(data)
        return self.jobs

if __name__ == '__main__':
    db = Database()
    countries = ['CANADA', 'USA']
    for country in countries:
        for job in Scraper(country = country).get_jobs(100):
            if job != 'Error':
                db.add_job(country = country, posting_info = job)
        expired_urls = db.get_job(country = country, date = True)
        for url in expired_urls:
            db.remove_job(country = country, url = url[0])