# This file contains the "Source" class which has a method for getting a list
#of all the text files in the "data folder"

import os

class Source:
    sources = []
    def getSources(self):
        d = os.getcwd()
        d = d.replace("API","data")
        sources = os.listdir(d)
        for i in range(0,len(sources)-1):
            d = os.getcwd()
            d = d.replace("API","data")
            d = d + "\\" + sources[i]
            sources[i] = d
        return sources
