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

    # Input the file name that need to be indexed
    def save_text2index(self, file_name):
        try:
            fo = codecs.open(file_name, encoding='utf-8', errors='strict')
            content = {"fileName": fo.name, "text": fo.read()}
            fo.close()
            self.es.index(index="test-index", doc_type='tweet', body=content)
            self.es.indices.refresh(index="test-index")
        # If the file if not valid "utf-8" file, do not index it
        except UnicodeDecodeError:
            pass

    # The method that search all files in the target directory than contain the query string list
    def search_func(self, query_string):
        result_dict = {}
        for root, subFolders, files in os.walk(TARGET_FOLDER):
            for dataFile in files:
                file_name = root + "/" + dataFile
                self.save_text2index(file_name)
            if len(files) > 0:
                res = self.es.search(index="test-index",
                                     body={"query": {"match": {"text": {"query": query_string, "operator": "and"}}}},
                                     size=10)
                self.es.indices.delete(index="test-index")
                for hit in res['hits']['hits']:
                    result_dict[hit["_source"]["fileName"]] = hit["_source"]["text"]
                    if len(result_dict) == 10:
                        return result_dict
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
        es_status = None
        time.sleep(10)
        while es_status is None:
            try:
                self.es.cluster.health(wait_for_status='yellow', request_timeout=40)
                es_status = 1
            except Exception as e:
                print e
                pass


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
        print "Start search the query strings in the target folder"
        result_list = search.search_func(query_strings)
        print 'The following files contain " ' + query_strings + ' ":'
        SearchStrings.print_helper(result_list)
    finally:
        # Always close the search engine
        p.kill()


if __name__ == '__main__':
    main()
