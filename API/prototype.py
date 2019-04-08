#This is the prototype of the AI. It is supposed to generate an extractive summary from a scientific paper.
#The current model is designed to read just neuroscience papers.
#The program takes a user-input question and outputs the 5 most related sentences from the text.
#A section from a sample text is used but in future implementations it could range from small papers to whole books

import re
import nltk
from nltk.stem import WordNetLemmatizer
import os 

wordnet_lemmatizer = WordNetLemmatizer()


#Definition of question class
class Question():
    userQuestion = ""
    wordsList = []
    usefulWords = []
    header = ""
    verbs = []
    wordnet_lemmatizer = WordNetLemmatizer()
    
    def getUserQuestion(self):
        #This function just gets the user question. Takes no parameters
        newQuestion = input("Please insert your question: ")
        self.userQuestion = newQuestion
        self.userQuestion = self.userQuestion.upper()

    def standardizeQuestion(self):
        punctuations="?:!.,;"
        self.wordsList = nltk.word_tokenize(self.userQuestion)
        for word in self.wordsList:
            if word in punctuations:
                self.wordsList.remove(word)

    def identifyHeader(self):
        #Identifies the header of the question
        self.header = self.wordsList[0]
        del self.wordsList[0]

    def removeArticles(self):
        #Removes the words that will not be compared
        #The words removed are particles that only work for grammatical puroposes but are not part of the meaning of the sentence
        temporary = nltk.pos_tag(self.wordsList)
        for idx, tag in enumerate(temporary):
            if (tag[1][:2]=="VB"):
                self.verbs.append(tag[0])
                del temporary[idx]
            self.usefulWords.append(temporary[idx][0])

        for word in self.usefulWords:
            if ((word == "A")or(word== "THE")or(word=="OF")or(word=="IN")):
                self.usefulWords.remove(word)
        

    def prepareCompare(self):
        #Calls other class functions to make a clean, word-split question
        self.standardizeQuestion()
        self.identifyHeader()
        self.removeArticles()
        #for word in self.verbs:
            #print(wordnet_lemmatizer.lemmatize(word,pos="v"))



class TextConverter():
    Text = ""
    sentenceList = []

    def __init__(self,t):
        self.Text = t
        
    def splitSentences(self):
        self.sentenceList = self.Text.split(".")

    def showSentences(self):
        print(self.sentenceList)

    def prepareCompare(self):
        self.Text = self.Text.upper()
        self.splitSentences()
        for idx in range(0,len(self.sentenceList)-1,1):
            sentence = self.sentenceList[idx]
            punctuations="?:!.,;"
            sentence_words = nltk.word_tokenize(sentence)
            for word in sentence_words:
                if word in punctuations:
                    sentence_words.remove(word)
            for i in range(0, len(sentence_words),1):
                sentence_words[i] = wordnet_lemmatizer.lemmatize(sentence_words[i],pos="v")
            self.sentenceList[idx] = sentence_words

    def compare(self,question):
        temporaryList = []
        similarity = {}
        maxSim = 0
        maxSimIdx = 0
        for idx in range(0, len(self.sentenceList)-1):
            counter = 0
            temporaryList = self.sentenceList[idx]
            simIndex = 0
            for idx2 in range(0, len(question)):
                if question[idx2] in temporaryList:
                    counter += 1
            try:
                simIndex = counter/len(temporaryList)
            except Exception:
                simIndex = 0
            similarity[idx]=simIndex
            if (simIndex > maxSim):
                maxSim = simIndex
                maxSimIdx = idx
        print("Here is my answer: ", self.sentenceList[maxSimIdx])

d = os.getcwd()
d = d.replace("API","data")
sources = []
sources = os.listdir(d)
for i in range(0, len(sources)-1):
    d = os.getcwd()
    d = d.replace("API","data")
    d = d + "\\" + sources[i]
    sources[i] = d
activeQuestion = Question()
activeQuestion.getUserQuestion()
activeQuestion.prepareCompare()
for file in sources:
    currentText = open(file,"r")
    entry = currentText.read()
    myText = TextConverter(entry)
    myText.prepareCompare()
    myText.compare(activeQuestion.usefulWords)
        



    

