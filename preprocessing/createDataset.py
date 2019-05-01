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
totWords=0

sentencesFormattedDataset=[]
sentencesOriginalDataset=[]
for filename in os.listdir(folder):
    xmldoc = minidom.parse(folder+'/'+filename)
    itemlist = xmldoc.getElementsByTagName('p')
    #retrieve all the p elements and create a single string 
    text=''
    for item in itemlist:
        text+=item.childNodes[0].data
    totWords += len(text)
    #preprocess the text:
    text=sentPros.removeParenthesis(text)
    text=sentPros.removeSpecialCharacters(text)
    text=sentPros.removeDoubleSpaces(text)
    sentencesList=text.split('.')
    formattedSentencesList=[]
    for idx, sentence in enumerate(sentencesList):
        print('original sentence:', sentence)
        lemmatizedSentence=sentPros.preprocessing(sentence)
        formattedSentencesList.append(lemmatizedSentence)
        print('formatted sentence:', lemmatizedSentence)
        print('\n')

    sentencesFormattedDataset.extend(formattedSentencesList)
    sentencesOriginalDataset.extend(sentencesList)

with open('dataset_original', 'wb') as f:
    pickle.dump(sentencesOriginalDataset, f)

with open('dataset_preprocessed', 'wb') as f:
    pickle.dump(sentencesFormattedDataset, f)

print('length text', totWords)
print('Done! Sentences in original dataset:', len(sentencesOriginalDataset))
print('Done! Sentences in formatted dataset:', len(sentencesFormattedDataset))
