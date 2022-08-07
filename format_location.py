from region_codes import country_codes

class CorrectFormatting:
    def __init__(self, country, location):
        self.codes = country_codes[f'{country}_CODES']
        self.location = location
    
    def format(self):
        for key, value in self.codes.items():
            self.location = self.location.replace(key, value)
        return self.location