#This is the prototype of the AI. It is supposed to generate an extractive summary from a scientific paper.
#The current model is designed to read just neuroscience papers.
#The program takes a user-input question and outputs the 5 most related sentences from the text.
#A section from a sample text is used but in future implementations it could range from small papers to whole books

import re

#Definition of question class
class Question():
    userQuestion = ""
    wordsList = []
    
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

    def prepareCompare(self):
        #Calls other class functions to make a clean, word-split question
        self.standardizeQuestion()
        self.splitQuestionWords()


#TODO clean question
#TODO clean text
#TODO compare text and questions (include some number crunching)
#TODO output results

activeQuestion = Question()
activeQuestion.getUserQuestion()
activeQuestion.prepareCompare()
activeQuestion.standardizeQuestion()
print(activeQuestion.wordsList)
