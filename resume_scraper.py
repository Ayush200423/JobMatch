import spacy
from PyPDF2 import PdfFileReader
import io

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load('./resumeparser/output/model-best')
        self.ents_dict = {
            'name': [],
            'fname': [],
            'lname': [],
            'phone': [],
            'college name': [],
            'degree': [],
            'graduation year': [],
            'years of experience': [],
            'company': [],
            'role': [],
            'skills': [],
            'location': []
        }
    
    def pdf_to_txt(self, resume_file):
        pdfFileObj = io.BytesIO(resume_file.read())
        pdfReader = PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0) 
        self.text = pageObj.extractText()
    
    def find_ents(self):
        doc = self.nlp(self.text)
        for ent in doc.ents:
            label = ent.label_
            if str(ent) in self.ents_dict[label.lower()] or label == 'email address':
                continue
            else:
                self.ents_dict[label.lower()].append(str(ent))
        try:
            self.ents_dict['fname'] = self.ents_dict['name'][0].split()[0]
            self.ents_dict['lname'] = self.ents_dict['name'][0].split()[1]
        except:
            self.ents_dict['fname'] = self.ents_dict['name']
            self.ents_dict['lname'] = ''
        return {key: ', '.join(value) if key != 'fname' and key != 'lname' and isinstance(value, list) else value for key, value in self.ents_dict.items()}