from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.qparser import OrGroup
from Utils.QueryParser import QueryParser as CustomQueryParser
from Utils.DocRanking import DocRanking

class WhooshQuery:
    def __init__(self):
        self.index = open_dir(".\\temp\\index")

    def ProcQuery(self, input):
        custom_query_parser = CustomQueryParser(input)
        max_hit = custom_query_parser.get_hits()
        key_words = custom_query_parser.get_key_words()

        doc_ranking = DocRanking()
        doc_ranking.set_index(self.index)

        with self.index.searcher() as searcher:
            query_parts = []
            for key_word in key_words:
                doc_ranking.add_terms(key_word)
                if " " in key_word:
                    query_parts.append(f'"{key_word}"')
                else:
                    query_parts.append(key_word)
            query_str = " ".join(query_parts)

            whoosh_parser = QueryParser("docContent", self.index.schema, group=OrGroup)
            whoosh_query = whoosh_parser.parse(query_str)

            results = searcher.search(whoosh_query, limit=10000)
            all_docs = [(result.docnum, result.score) for result in results]
            print(f"Debug: Found {len(all_docs)} raw results")

            print(f"Total hits: {min(len(all_docs), max_hit)}")
            score_docs = doc_ranking.get_my_score_docs(all_docs, max_hit)
            print(f"Debug: Processed {len(score_docs)} scored docs")

            rank = 0
            for docnum, score in score_docs:
                rank += 1
                doc = searcher.stored_fields(docnum)
                print(f"{rank} [{score}] ", end="")
                print(doc.get("docNo", "N/A"))
                file_content = doc.get("docContent", "").replace("\n", " ").replace("\r", " ")  
                file_content = doc.get("docContent", "")
                if len(file_content) > 500:
                    print(file_content[:500] + "...")
                else:
                    print(file_content)
                print("----------------------------------------------------------------------")