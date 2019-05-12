'''
This script is used to convert pdfs parsed as xml to create a single text file from all the sources.
'''
from xml.dom import minidom
import sentenceProcessing as sentPros
import os
import re
import pickle
import json

xmlFolder='xml2text'
dataFile='dataset_qa'
jsonFile="test_dataset.json"

datasetText=""
#Used just to see how many words in the original dataset
totWords=0

def removeParenthesis(data):
    #Remove text between parehtesis
    formattedData=re.sub(r" ?\([^)]+\)", "", data)
    return formattedData

if __name__ == "__main__":
    #Iterate through .xml files and extract the text
    for filename in os.listdir(xmlFolder):
        print('Processing', filename)
        #Parse the xml doc and retrieve all the p elements in a list
        xmldoc = minidom.parse(xmlFolder+'/'+filename)
        itemlist = xmldoc.getElementsByTagName('p')
        #Iterate through the p elements, extract their text and append to a string 
        text=''
        for item in itemlist:
            text+=item.childNodes[0].data
        datasetText += removeParenthesis(text)

    totWords=len(datasetText)

    #get the text from the hand-created QA dataset
    print('processing', dataFile)
    datasetfile=open(dataFile, 'r')
    dataset_string=datasetfile.read()
    datasetText += removeParenthesis(dataset_string)
    totWords += len(dataset_string)

    print('Processing', jsonFile)
    #get the text from the .json file
    with open(jsonFile) as json_file:  
        data = json.load(json_file)
        for QA in data:
            datasetText += removeParenthesis(QA['answer'])
            totWords += len(QA['answer'])

    with open('dataset.txt', 'w') as f:
        f.write(datasetText)


    print('Number of chars in the dataset:', totWords)
