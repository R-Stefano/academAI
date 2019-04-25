'''
This script is used to convert pdfs parsed as xml to txt files.
This script iterates through each .xml file in xml2text folder.
It creates a .txt file which contains all the text found in the .xml file.
'''
from xml.dom import minidom
import os
import re
folder='xml2text'
targetFolder='texts'
totWords=0

def removeParenthesis(data):
    #Remove text between parehtesis
    formattedData=re.sub(r" ?\([^)]+\)", "", data)
    #Remove text that comes before ) or after (
    formattedData=re.sub('(\(.+|.+\))','',formattedData)
    return formattedData

def removeSpecialCharacters(data):
    #substitute all the characters that are not letters, numbers, white space, %, ., :, ,, " or -  with a space
    return re.sub(r'[^a-zA-Z0-9\s%\.:,"\-]','',data)

for filename in os.listdir(folder):
    xmldoc = minidom.parse(folder+'/'+filename)
    itemlist = xmldoc.getElementsByTagName('p')
    text=''
    for item in itemlist:
        data=item.childNodes[0].data
        data=removeParenthesis(data)
        data=removeSpecialCharacters(data)
        text+=data
    totWords += len(text)
    filename=filename[:filename.find('.pdf')]
    with open(targetFolder+'/'+filename+'.txt', 'w') as f:
        f.write(text)

print('length text', totWords)

