'''
This script is used to convert pdfs parsed as xml to create a single text file from all the sources.
'''
from xml.dom import minidom
import os
import re
import pickle
import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 

xmlFolder='xml2text'
dataFile='dataset_qa'
jsonFile="test_dataset.json"

#Used just to see how many words in the original dataset
sentences=0
lengthSentences=0

def datasetAnalysis(listParagraphs):
    Nparagraphs=len(listParagraphs)
    Distrib_N_Sent_Paragraphs=[]
    Distrib_N_Words_Paragraphs=[]
    Distrib_N_Words_Sentences=[]
    uniqueWords={}
    totNofWords=0

    for p in listParagraphs:
        print(p)
        p=p.lower()
        #substitute all the characters that are not letters, numbers, white space, %, or dots with a space
        p=re.sub(r'[^a-zA-Z0-9\s%\-\.]','',p)
        paragSentences=p.split('.')
        Distrib_N_Sent_Paragraphs.append(len(paragSentences))
        totWords=0
        for s in paragSentences:
            print(s)
            sentenceWords=s.split()
            totWords+=len(sentenceWords)
            Distrib_N_Words_Sentences.append(len(sentenceWords))
            for w in sentenceWords:
                if w not in uniqueWords:
                    uniqueWords[w]=1
                else:
                    uniqueWords[w] += 1
        
        Distrib_N_Words_Paragraphs.append(totWords)
        totNofWords += totWords
    
    print('Number paragraphs', Nparagraphs)
    
    #Display number of sentences in paragraphs
    plt.hist(Distrib_N_Sent_Paragraphs)
    plt.xlabel('Number sentences in each paragraph')
    plt.ylabel('Number of paragraphs')
    plt.show()
    ##Display number of sentences in paragraphs
    plt.hist(Distrib_N_Words_Paragraphs)
    plt.xlabel('Number words in each paragraph')
    plt.ylabel('Number of paragraphs')
    plt.show()

    #Smooth Inverse Frequency weighting
    print('Number unique words', len(uniqueWords))
    totValTest=0
    for key in uniqueWords:
        uniqueWords[key] /=totNofWords
        totValTest +=uniqueWords[key]

    return uniqueWords


def removeParenthesis(data):
    #Remove text between parehtesis
    formattedData=re.sub(r" ?\([^)]+\)", "", data)
    return formattedData

if __name__ == "__main__":
    paragraphsList=[]
    #Iterate through .xml files and extract the text
    for filename in os.listdir(xmlFolder):
        print('Processing', filename)
        #Parse the xml doc and retrieve all the p elements in a list
        xmldoc = minidom.parse(xmlFolder+'/'+filename)
        itemlist = xmldoc.getElementsByTagName('p')
        #Iterate through the p elements, extract their text and append to a string 
        for item in itemlist:
            parag=removeParenthesis(item.childNodes[0].data)
            paragraphsList.append(parag)

    '''
    #get the text from the hand-created QA dataset
    print('processing', dataFile)
    datasetfile=open(dataFile, 'r')
    dataset_string=datasetfile.read()
    datasetText += removeParenthesis(dataset_string)
    totWords += len(dataset_string)
    '''
    print('Processing', jsonFile)
    #get the text from the .json file
    with open(jsonFile) as json_file:  
        data = json.load(json_file)
        for QA in data:
            paragraphsList.append(removeParenthesis(QA['answer']))

    df = pd.DataFrame(paragraphsList, columns = ['Text']) 
    df.to_csv('dataset.csv')

    wordsProb=datasetAnalysis(paragraphsList)

    with open('wordsProb.json', 'w') as f:
        json.dump(wordsProb, f)
