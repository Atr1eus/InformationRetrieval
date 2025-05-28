class SGMLParser:
    def __init__(self, file_content):
        self.doc_no = self.extract_tag(file_content, "<DOCNO>", "</DOCNO>")
        self.doc_type = self.extract_tag(file_content, "<DOCTYPE>", "</DOCTYPE>")
        self.txt_type = self.extract_tag(file_content, "<TXTTYPE>", "</TXTTYPE>")
        self.doc_content = self.extract_tag(file_content, "<TEXT>", "</TEXT>")

    def extract_tag(self, content, start_tag, end_tag):
        start = content.find(start_tag) + len(start_tag)
        end = content.find(end_tag)
        return content[start:end].strip()

    def get_doc_no(self):
        return self.doc_no

    def get_doc_type(self):
        return self.doc_type

    def get_txt_type(self):
        return self.txt_type

    def get_doc_content(self):
        return self.doc_content