import spacy
from PyPDF2 import PdfFileReader
import io

class ResumeParser:
    def __init__(self):
        self.nlp = spacy.load('./resumeparser/output/model-best')
    
    def pdf_to_txt(self, resume_file):
        pdfFileObj = io.BytesIO(resume_file.read())
        pdfReader = PdfFileReader(pdfFileObj)
        pageObj = pdfReader.getPage(0) 
        self.text = pageObj.extractText()
        resume_text = self.text.strip()
        replace_values = [[' ,', ', '], ['  ', ' ']]
        for old_val, new_val in replace_values:
            resume_text = resume_text.replace(old_val, new_val)
        text_encoded = resume_text.encode("ascii", "ignore")
        text_decoded = text_encoded.decode()
        return text_decoded
    
    def find_ents(self):
        ents_dict = {
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
        doc = self.nlp(self.text)
        for ent in doc.ents:
            label = ent.label_
            if str(ent) in ents_dict[label.lower()] or label == 'email address':
                continue
            else:
                ents_dict[label.lower()].append(str(ent))
        try:
            ents_dict['fname'] = ents_dict['name'][0].split()[0]
            ents_dict['lname'] = ents_dict['name'][0].split()[1]
        except:
            ents_dict['fname'] = ents_dict['name']
            ents_dict['lname'] = ''
        return {key: ', '.join(value) if key != 'fname' and key != 'lname' and isinstance(value, list) else value for key, value in ents_dict.items()}