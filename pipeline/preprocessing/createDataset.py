'''
This script is used to convert pdfs parsed as xml to create the dataset.
This script iterates through each .xml file in xml2text folder splitting the sentences 
and applying all the preprocessing steps that the sentence must go through
'''
from xml.dom import minidom
import sentenceProcessing as sentPros
import os
import re
import pickle

folder='xml2text'
QAFile='dataset_qa'
#Used just to see how many words in the original dataset
totWords=0

#Stores the lemmatized and not lemmatized sentences
sentencesFormattedDataset=[]
sentencesOriginalDataset=[]

def preprocessText(originalText, sentencesOriginalDataset, sentencesFormattedDataset):
    text=sentPros.removeParenthesis(originalText)
    text=sentPros.removeSpecialCharacters(text)
    text=sentPros.removeDoubleSpaces(text)
    sentencesList=text.split('.')
    formattedSentencesList=[]
    for idx, sentence in enumerate(sentencesList):
        lemmatizedSentence=sentPros.preprocessing(sentence)
        formattedSentencesList.append(lemmatizedSentence)

    #Store the not lemmatized text and the lemmatized one. 
    #not lemmatized is used to display the results, the lemmatized to compute similarity
    sentencesFormattedDataset.extend(formattedSentencesList)
    sentencesOriginalDataset.extend(sentencesList)

    return sentencesOriginalDataset, sentencesFormattedDataset

#Iterate through .xml files and extract the text
for filename in os.listdir(folder):
    print('Processing', filename)
    #Parse the xml doc and retrieve all the p elements in a list
    xmldoc = minidom.parse(folder+'/'+filename)
    itemlist = xmldoc.getElementsByTagName('p')
    #Iterate through the p elements, extract their text and append to a string 
    text=''
    for item in itemlist:
        text+=item.childNodes[0].data
    totWords += len(text)
    sentencesOriginalDataset, sentencesFormattedDataset=preprocessText(text, sentencesOriginalDataset, sentencesFormattedDataset)

#get the text from the hand-created QA dataset
print('processing ')
datasetfile=open(QAFile, 'r')
dataset_string=datasetfile.read()
totWords += len(dataset_string)
sentencesOriginalDataset, sentencesFormattedDataset=preprocessText(dataset_string, sentencesOriginalDataset, sentencesFormattedDataset)

with open('dataset_original', 'wb') as f:
    pickle.dump(sentencesOriginalDataset, f)

with open('dataset_preprocessed', 'wb') as f:
    pickle.dump(sentencesFormattedDataset, f)

print('Original text length', totWords)
print('Done! Sentences in original dataset:', len(sentencesOriginalDataset))
print('Done! Sentences in formatted dataset:', len(sentencesFormattedDataset))
