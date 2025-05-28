import re

class QueryParser:
    def __init__(self, query):
        self.hits = 10
        self.key_words = []
        terms = query.split()
        if terms[0] == "search":
            i = 1
            while i < len(terms):
                term = terms[i]
                if term.startswith('"'):
                    phrase = term
                    while not term.endswith('"') and i < len(terms) - 1:
                        i += 1
                        term = terms[i]
                        phrase += " " + term
                    self.key_words.append(self.sanitize_query(phrase.replace('"', '')))
                elif term.startswith("--"):
                    if term.startswith("--hits=="):
                        self.hits = int(term[8:])
                    else:
                        raise Exception("Not a valid hits")
                else:
                    self.key_words.append(self.sanitize_query(term))
                i += 1
        else:
            raise Exception("Not a valid query")

    def sanitize_query(self, query):
        return re.sub(r'\d+', '', query).replace(r'[^\w\s]', ' ').lower()

    def get_hits(self):
        return self.hits

    def get_key_words(self):
        return self.key_words