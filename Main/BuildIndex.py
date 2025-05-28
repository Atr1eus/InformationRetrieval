import os
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, KEYWORD, STORED, NUMERIC
from Utils.SGMLParser import SGMLParser

def build_index():
    # 定义 Whoosh 的 Schema
    schema = Schema(
        fileName=TEXT(stored=True),
        filePath=STORED,
        fileSize=NUMERIC(stored=True),
        docNo=STORED,
        docType=KEYWORD(stored=True),
        txtType=KEYWORD(stored=True),
        docContent=TEXT(stored=True)
    )

    # 创建索引目录
    if not os.path.exists(".\\temp\\index"):
        os.makedirs(".\\temp\\index")
    index = create_in(".\\temp\\index", schema)

    # 创建 Whoosh 索引写入器
    writer = index.writer()

    # 遍历文件并添加到索引
    total_path = "E:\\InformationRetrieval\\final_assignment\\code\\tdt3"
    for root, dirs, files in os.walk(total_path):
        for file in files:
            file_path = os.path.join(root, file)
            with open(file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            sgml_parser = SGMLParser(file_content)

            # 添加文档到索引
            writer.add_document(
                fileName=file,
                filePath=file_path,
                fileSize=os.path.getsize(file_path),
                docNo=sgml_parser.get_doc_no(),
                docType=sgml_parser.get_doc_type(),
                txtType=sgml_parser.get_txt_type(),
                docContent=sgml_parser.get_doc_content()
            )

    # 提交更改
    writer.commit()

if __name__ == "__main__":
    build_index()