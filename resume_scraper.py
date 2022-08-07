import spacy
from PyPDF2 import PdfReader

class ResumeParser:
    def __init__(self, file_path):
        self.nlp = spacy.load('./resumeparser/output/model-best')
        self.file = file_path
    
    def pdf_to_txt(self):
        reader = PdfReader(self.file)
        page = reader.pages[0]
        self.text = page.extract_text()
    
    def find_ents(self):
        doc = self.nlp(self.text)
        for ent in doc.ents:
            print(ent.text, ent.label_)