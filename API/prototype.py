#This is the prototype of the AI. It is supposed to generate an extractive summary from a scientific paper.
#The current model is designed to read just neuroscience papers.
#The program takes a user-input question and outputs the 5 most related sentences from the text.
#A section from a sample text is used but in future implementations it could range from small papers to whole books

import re

#Definition of question class
class Question():
    userQuestion = ""
    wordsList = []
    usefulWords = []
    header = ""
    
    def getUserQuestion(self):
        #This function just gets the user question. Takes no parameters
        newQuestion = input("Please insert your question: ")
        self.userQuestion = newQuestion

    def splitQuestionWords(self):
        #This function splits the question's words into a list
        localQuestionList = []
        localQuestionList = self.userQuestion.split(" ")
        self.wordsList = localQuestionList

    def standardizeQuestion(self):
        #This function eliminates all non alphabetic characters
        cleanUserQuestion = self.userQuestion
        regex = re.compile('[^a-zA-Z]')
        cleanUserQuestion = regex.sub(' ',cleanUserQuestion)
        cleanUserQuestion = cleanUserQuestion.upper()
        self.userQuestion = cleanUserQuestion

    def identifyHeader(self):
        #Identifies the header of the question
        self.header = self.wordsList[0]
        del self.wordsList[0]

    def ghostToast(self):
        #Useless function used to cheat so the try/except method actually works
        a = 0

    def removeArticles(self):
        #Removes the words that will not be compared
        #The words removed are particles that only work for grammatical puroposes but are not part of the meaning of the sentence
        try:
            self.wordsList.remove("A")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("THE")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("OF")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("THIS")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("THESE")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("FOR")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("IN")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("AT")
        except:
            self.ghostToast()
        try:
            self.wordsList.remove("")
        except:
            self.ghostToast()

    def setUsefulWords(self):
        #Defines the final list of words that will be compared to the text
        self.usefulWords = self.wordsList
        

    def prepareCompare(self):
        #Calls other class functions to make a clean, word-split question
        self.standardizeQuestion()
        self.splitQuestionWords()
        self.identifyHeader()
        self.removeArticles()
        self.setUsefulWords()
        print("Comparing useful words = " , self.usefulWords)
        print("The header of the question is: ", self.header)


activeQuestion = Question()
activeQuestion.getUserQuestion()
activeQuestion.prepareCompare()
