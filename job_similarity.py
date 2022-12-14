import spacy
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

from database.jobs_database import JobsDatabase

class Similarity:
    def __init__(self, role, location, resume_data):
        location_separate = location.split(', ')
        self.role = role.split()
        self.region = location_separate[0]
        self.country = location_separate[1]
        self.resume_data = resume_data
        self.nlp = spacy.load('en_core_web_md', exclude = ["tagger", "parser", "senter", "attribute_ruler", "lemmatizer", "ner"])
        self.stop_words = set(stopwords.words('english'))
        self.resume_doc = self.nlp_resume_doc()
        self.db = JobsDatabase()
        self.db_search_results = set()
        self.similarity_threshold = 0.85
        self.jobs = []

    def nlp_resume_doc(self):
        resume_tokens = word_tokenize(self.resume_data)
        filtered_resume = ' '.join([word for word in resume_tokens if not word.lower() in self.stop_words])
        resume_doc = self.nlp(filtered_resume)
        return resume_doc

    def get_jobs(self):
        for word in self.role:
            job_urls = self.db.get_job(country = self.country, role = f'%{word}%', region = f'%{self.region}')
            self.db_search_results = {url_tuple[0] for url_tuple in job_urls}
            for url in self.db_search_results:
                posting = self.db.get_job(country = self.country, url = url)
                similarity = self.get_similarity(posting['description'])
                if similarity > self.similarity_threshold:
                    self.jobs.append([posting, similarity])
        if len(self.jobs) < 5 and self.region != '':
            self.region = ''
            self.jobs = []
            self.get_jobs()
        return self.jobs

    def get_similarity(self, posting_data):
        posting_tokens = word_tokenize(posting_data)
        filtered_posting = ' '.join([word for word in posting_tokens if not word.lower() in self.stop_words])
        posting_doc = self.nlp(filtered_posting)
        similarity = self.resume_doc.similarity(posting_doc)
        return similarity