# This piece of code contains the retriever. It is written as a module with a
# function that can be imported and then executed by a cgi script.

import lucene
from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import IndexReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def get_results(terms, path_to_index):
    # Initialize
    lucene.initVM()
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    reader = IndexReader.open(SimpleFSDirectory(File(path_to_index)))
    searcher = IndexSearcher(reader)
    parser = QueryParser(Version.LUCENE_CURRENT, "text", analyzer)

    # Do the search
    query = parser.parse(parser.escape(terms))
    hits = searcher.search(query,100)
    count = 1
    reply = ''
    for scoreDoc in hits.scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        reply += '<div style="display:inline-block"> <img src="{0}" width="200"/></div>'.format("../common_image_base/" + doc.get("url"))
        count += 1
    return reply
