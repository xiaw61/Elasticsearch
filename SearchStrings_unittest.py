__author__ = 'xiaw'

import unittest

from SearchStrings import *

ELASTICSEARCH_LAUNCH_CMD = './elasticsearch-1.3.4/bin/elasticsearch'


class SearchStringsTest(unittest.TestCase):
    def test(self):

        search = SearchStrings()
        try:
            p = subprocess.Popen([ELASTICSEARCH_LAUNCH_CMD], stdin=PIPE, stderr=PIPE, stdout=PIPE, shell=True)
            search.is_elasticsearch_ready()

            # case 0
            # No query string
            result_list = search.search_func([""])
            result = '\n'.join(result_list.keys())

            self.assertEqual(result, "")

            # case 1
            # Result has less than 10
            result_list = search.search_func(["rousseaua@immunex.com"])
            result = True
            reference1 = ["news/sci.med/58057", "news/sci.med/58056", "news/sci.med/59232", "news/sci.med/58987"]
            for it in result_list:
                if it not in reference1:
                    result = False
                    break
            self.assertEqual(result, True)
        except:
            pass
        finally:
            p.kill()


if __name__ == '__main__':
    unittest.main()