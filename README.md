Elasticsearch
=============

Make The 20 Newsgroups Data Set searchable
This program run on Unix-like OS with at least Java 7 and python

1.Install elasticsearch python library :   pip install elasticsearch

2.Move the file you want to search into the "target_folder";
  
3.run : python SearchString.py  [string ...]
  e.g: python SearchString.py  or is
  
4.unittest command: python SearchStrings_unittest.py 
  

PS:
In order to reduce the searching time, once find 10 files contain the search query, 
the program will stop search and print out the 10 files name.