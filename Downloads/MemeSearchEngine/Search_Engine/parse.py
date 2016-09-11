#!/usr/bin/env python
# to run this code do
# `python parse.py <path to image->ocr file> <path to image->labels file> <path to index>`
# An index would be created at <path to index>.

import os
import sys
import lucene
from lxml import html
from lxml import etree

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version

def getdata(ocrtext, labels):
    dataset = {}
    imglbl = {}
    
    # Read the labels file
    with open(labels, "rb") as f:
        for line in f.readlines():
            spl = line.split()
            imglbl[spl[1]] = ' '.join(spl[2].split('-'))
    
    # Read the ocr text file and append labels wherever they exists.
    with open(ocrtext, "rb") as f:
        data = f.readlines()
        for line in data:
            split_line = line.split("#")
            if split_line[0] in imglbl:
                split_line[1] = split_line[1].rstrip() + " " + imglbl[split_line[0]].lower()
            dataset[split_line[0]] = split_line[1].rstrip()
    return dataset


def get_data(ocrtext, labels):
    dataset = getdata(ocrtext, labels)

    for key in dataset:
        doc = Document()
        print key, dataset[key]
        doc.add(Field("url", key, Field.Store.YES, Field.Index.NOT_ANALYZED))
        doc.add(Field("text", dataset[key], Field.Store.NO, Field.Index.ANALYZED))
        writer.addDocument(doc)

if __name__ == "__main__":
    lucene.initVM()
    indexDir = SimpleFSDirectory(File(sys.argv[3]))
    writerConfig = IndexWriterConfig(Version.LUCENE_CURRENT, StandardAnalyzer(Version.LUCENE_CURRENT))
    writer = IndexWriter(indexDir, writerConfig)
    get_data(sys.argv[1], sys.argv[2])
    writer.close()
