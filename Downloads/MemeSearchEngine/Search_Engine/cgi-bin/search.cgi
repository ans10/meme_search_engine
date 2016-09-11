#!/usr/bin/env python
import cgi
import os
import sys

# This is necessary on systems where you don't have root and need to specify path to the
# pylucene egg file.
# This can be commented out if pylucene is installed on your system as root.
#sys.path.append('/home/<username>/.local/lib64/python/lucene-4.10.1-py2.6-linux-x86_64.egg')

# import the search.py file that returns the search results
import search

# update path to index and name of the directory of documents here
path_to_index = "index"

# get values in POST request
form = cgi.FieldStorage()
terms = form.getvalue("terms", "none")

# escape terms
escaped_terms = cgi.escape(terms) #escapes <>&
escaped_terms = escaped_terms.translate(None, "*?./") #filters *?./

print "Content-type: text/html"
print

print """
<html>

<head>
<title>Super Awesome Results</title>
<h1 style="text-align:left;float:left;">Results for query <u>{0}</u></h1><a style="text-align:right;float:right;" href=\"\\search.html\">Back</a><hr style="clear:both;"/>
</head>

<body>
{1}
</body>

</html>
""".format(escaped_terms, search.get_results(escaped_terms, path_to_index))

