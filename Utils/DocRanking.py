import math

class DocRanking:
    def __init__(self):
        self.terms = []
        self.my_score_docs = []
        self.index = None
        self.avg_content_size = 0
        self.doc_sizes = {}  # 缓存文档大小

    def add_terms(self, term):
        self.terms.append(term)

    def set_index(self, index):
        self.index = index

    def set_my_score_docs(self, all_docs):
        with self.index.searcher() as searcher:
            for docnum, _ in all_docs:
                score = self.get_score(docnum, searcher)
                self.my_score_docs.append((docnum, score))
            self.my_score_docs.sort(key=lambda x: x[1], reverse=True)

    def get_my_score_docs(self, all_docs, hits):
        self.set_avg_content_size()
        self.set_my_score_docs(all_docs)
        return self.my_score_docs[:hits]

    def get_term_freq(self, docnum, term, searcher):
        doc_content = searcher.stored_fields(docnum).get("docContent", "")
        words = doc_content.split()
        return sum(1 for word in words if word.lower() == term.lower())

    def get_doc_freq(self, term, searcher):
        return searcher.doc_frequency("docContent", term.lower())

    def get_doc_num(self, searcher):
        return searcher.doc_count()

    def get_content_size(self, docnum, searcher):
        if docnum not in self.doc_sizes:
            doc_content = searcher.stored_fields(docnum).get("docContent", "")
            self.doc_sizes[docnum] = len(doc_content.split())
        return self.doc_sizes[docnum]

    def set_avg_content_size(self):
        with self.index.searcher() as searcher:
            num_docs = self.get_doc_num(searcher)
            total_content_size = sum(self.get_content_size(docnum, searcher) for docnum in range(num_docs))
            self.avg_content_size = total_content_size / num_docs if num_docs > 0 else 1

    def get_bm25(self, docnum, term, searcher):
        term_freq = self.get_term_freq(docnum, term, searcher)
        doc_freq = self.get_doc_freq(term, searcher)
        content_size = self.get_content_size(docnum, searcher)
        k1 = 1.2
        b = 0.75
        K = k1 * (1 - b + b * content_size / self.avg_content_size)
        tf = term_freq * (1 + k1) / (K + term_freq)
        idf = math.log((self.get_doc_num(searcher) - doc_freq + 0.5) / (doc_freq + 0.5)) if doc_freq > 0 else 0
        return tf * idf

    def get_score(self, docnum, searcher):
        return sum(self.get_bm25(docnum, term, searcher) for term in self.terms)