__author__ = 'xiaw'
import os
import sys
import codecs
import subprocess
import time
from subprocess import PIPE

from elasticsearch import Elasticsearch


TARGET_FOLDER = "target_folder"
ELASTICSEARCH_LAUNCH_CMD = './elasticsearch-1.3.4/bin/elasticsearch'


class SearchStrings:
    def __init__(self):
        self.es = Elasticsearch()

    def save_text2engine(self):
        for root, subFolders, files in os.walk(TARGET_FOLDER):
            for dataFile in files:
                file_name = root + "/" + dataFile
                try:
                    fo = codecs.open(file_name, encoding='utf-8', errors='strict')
                    content = {"fileName": fo.name, "text": fo.read()}
                    fo.close()
                    self.es.index(index="test-index", doc_type='tweet', body=content, id=file_name)
                    self.es.indices.refresh(index="test-index")
                # If the file if not valid "utf-8" file, do not index it
                except UnicodeDecodeError:
                    pass

    # The method that search all files in the target directory than contain the query string list
    def search_func(self, query_string):
        result_dict = {}
        res = self.es.search(index="test-index",
                             body={"query": {"match": {"text": {"query": query_string, "operator": "and"}}}},
                             size=10)
        # self.es.indices.delete(index="test-index")
        for hit in res['hits']['hits']:
            result_dict[hit["_source"]["fileName"]] = hit["_source"]["text"]
        return result_dict

    # convert the direction to string in print format
    @staticmethod
    def print_helper(result_list):
        i = 1
        for key in result_list:
            print str(i) + "th file:" + key
            i += 1

    # finish when the search engine is ready to use
    def is_elasticsearch_ready(self):
        print "Checking whether search engine is ready..."
        time.sleep(20)
        self.es.cluster.health(wait_for_status='yellow', request_timeout=120)

def main():
    if len(sys.argv) < 2:
        print "Please input the search strings"
        sys.exit(1)

    search = SearchStrings()
    query_strings = " ".join(sys.argv[1:])

    result_list = None
    p = None
    try:
        print "Launch the search engine..."
        p = subprocess.Popen([ELASTICSEARCH_LAUNCH_CMD], stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
        search.is_elasticsearch_ready()
        print "Indexing the target files to search engine"
        search.save_text2engine();

        print "Start search the query strings in the target folder"
        result_list = search.search_func(query_strings)

        print 'The following files contain " ' + query_strings + ' ":'
        SearchStrings.print_helper(result_list)
    finally:
        # Always close the search engine
        search.es.nodes.shutdown(node_id="_all")


if __name__ == '__main__':
    main()
