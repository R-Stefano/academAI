#This is the question class
# It is designed to get the user question, clean it from punctuation, lemmatize it
# and return a list of the words that will be used during the comparison with the texts

import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

class Question():
    user_question = ""
    complete_list = []
    useful_list = []
    header = ""

    def poseQuestion(self, question):
        self.user_question=question
        self.prepareCompare()
        return self.useful_list

    def prepareCompare(self):
        #This function aims to remove punctuation and to capitalize and lemmatize the words
        #It calls the respective sub-functions
        self.user_question = self.user_question.lower()
        self.tokenizeSentence()
        self.removePunctuation()
        self.identifyHeader()
        self.removeArticles()
        self.lemmatizeWords()

    def tokenizeSentence(self):
        #This function splits the words into elements of a list called words_list
        self.complete_list = nltk.word_tokenize(self.user_question)
        self.useful_list = self.complete_list

    def removePunctuation(self):
        #This function removes the punctuation from the list
        punctuation = "?:!.,;()\""
        for word in self.complete_list:
            if word in punctuation:
                self.useful_list.remove(word)

    def identifyHeader(self):
        #This function identifies the header of the question
        #TODO improve sentence comparison with rewards for matching the question-header realted words
        self.header = self.complete_list[0]

    def removeArticles(self):
        #This function removes the articles that are used for grammar purpose but serve no big part in meaning purposes
        #They are removed to avoid sentence matching based on meaningless articles
        #TODO after evaluation check if it necessary to remove more particles
        #TODO check if this particles can be used somewhere else
        particles = ["the","a","of","in"]
        for word in self.useful_list:
            if word in particles:
                self.useful_list.remove(word)
        
    def lemmatizeWords(self):
        #lemmatizes useful list
        lemmatized_words = []
        for word in self.useful_list:
            new_word = wordnet_lemmatizer.lemmatize(word,pos = "v")
            lemmatized_words.append(new_word)
            self.useful_list = lemmatized_words
            
