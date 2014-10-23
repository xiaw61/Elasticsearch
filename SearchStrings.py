__author__ = 'xiaw'
import codecs
import subprocess
import httplib
import time
from subprocess import *

from elasticsearch import Elasticsearch

es = Elasticsearch()
TARGET_FOLDER = "news"


class SearchStrings:
    @staticmethod
    def get_query_string():
        queryStrs = ""
        for queryString in sys.argv[1:]:
            queryStrs += queryString + " "
        return queryStrs

    def searchfunc(self, query_string):
        result_dict = {}
        for root, subFolders, files in os.walk(TARGET_FOLDER):
            for dataFile in files:
                fileName = root + "/" + dataFile
                try:
                    fo = codecs.open(fileName, encoding='utf-8', errors='strict')
                    content = {
                        "fileName": fo.name,
                        "text": fo.read()
                    }
                    fo.close()
                    res = es.index(index="test-index", doc_type='tweet', body=content)
                    es.indices.refresh(index="test-index")
                except UnicodeDecodeError:
                    pass
            if len(files) > 0:
                res = es.search(index="test-index",
                                body={"query": {"match": {"text": {"query": query_string, "operator": "and"}}}},
                                size=10)
                es.indices.delete(index="test-index")
                for hit in res['hits']['hits']:
                    result_dict[hit["_source"]["fileName"]] = hit["_source"]["text"]
                    if len(result_dict) == 10:
                        break

            if len(result_dict) == 10:
                break
        return result_dict

    @staticmethod
    def print_helper(result_list):
        i = 1
        for key in result_list:
            print i, "th file ", key, ":\n", result_list[key], "\n"
            i += 1

    def main(self):
        query_strings = self.get_query_string()
        result_list = None
        try:
            p = subprocess.Popen(['./elasticsearch-1.3.4/bin/elasticsearch'], stdin=PIPE, stderr=PIPE, stdout=PIPE,
                                 shell=True)
            es_status = None
            while es_status is None:
                try:
                    time.sleep(5)
                    h1 = httplib.HTTPConnection("localhost:9200")
                    h1.request("get", "status")
                    es_status = 1
                    h1.close()
                except:
                    pass
            result_list = self.searchfunc(query_strings)
            self.print_helper(result_list)

        finally:
            p.kill()


if __name__ == '__main__':
    s = SearchStrings()
    s.main()
