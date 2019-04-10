#This file contains the class "Information"
#The purpose of this class is to clean and lemmatize the sentences from a .txt file
#The resulting phrases will then be compared agains the words the program searches from the question

import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

class Information:
    text = ""
    complete_list = []
    useful_list = []

    def __init__(self,text):
        self.text = text

    def prepareCompare(self):
        self.text = self.text.lower()
        self.splitSentences()
        self.tokenizeSentence()
        self.removePunctuation()
        self.removeArticles()
        self.lemmatizeWords()
        
    def splitSentences(self):
        self.complete_list = self.text.split(".")
        
    def tokenizeSentence(self):
        #This function splits the words into elements of a list called words_list
        temporary_list = []
        for sentence in self.complete_list:
            new_sentence = nltk.word_tokenize(sentence)
            temporary_list.append(new_sentence)
        self.complete_list = temporary_list
        self.useful_list = self.complete_list
    
    def removePunctuation(self):
        #This function removes the punctuation from the list
        punctuation = "?:!.,;()\""
        for sentence in self.useful_list:
            for word in sentence:
                if word in punctuation:
                    sentence.remove(word)
                    

    def removeArticles(self):
        #This function removes the articles that are used for grammar purpose but serve no big part in meaning purposes
        #They are removed to avoid sentence matching based on meaningless articles
        #TODO after evaluation check if it necessary to remove more particles
        #TODO check if this particles can be used somewhere else
        particles = ["the","a","of","in"]
        for word in self.useful_list:
            if word in particles:
                self.useful_list.remove(word)
            if (len(word)==0):
                self.useful_list.remove(word)

    def lemmatizeWords(self):
        #lemmatizes useful list
        lemmatized_sentences = []
        for sentence in self.useful_list:
            lemmatized_words = []
            for word in sentence:
                new_word = wordnet_lemmatizer.lemmatize(word,pos = "v")
                lemmatized_words.append(new_word)
            lemmatized_sentences.append(lemmatized_words)
        self.useful_list = lemmatized_sentences

    def getUsefulText(self):
        return self.useful_list


