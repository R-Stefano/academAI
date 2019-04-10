#This file contains the class "Information"
#The purpose of this class is to clean and lemmatize the sentences from a .txt file
#The resulting phrases will then be compared agains the words the program searches from the question

import nltk
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()

class Information:
    def __init__(self,text):
        self.text = text
        self.complete_list = []
        self.useful_list = []

    def prepareCompare(self):
        self.splitSentences()
        self.tokenizeSentence()
        
    def splitSentences(self):
        self.complete_list = self.text.split(".")
        
    def tokenizeSentence(self):
        #This function splits the words into elements of a list called words_list
        for sentence in self.complete_list:
            sentence=sentence.lower()
            sentence=self.removePunctuation(sentence)
            sentence_tokens = nltk.word_tokenize(sentence)
            useful_tokens=self.removeArticles(sentence_tokens)
            lemmatized_tokens=self.lemmatizeWords(useful_tokens)
            self.useful_list.append(lemmatized_tokens)
    
    def removePunctuation(self, sentence):
        #This function removes the punctuation from the list
        punctuation = "?:!.,;()\""
        for character in sentence:
            if character in punctuation:
                sentence=sentence.replace(character, '')
        return sentence
                    

    def removeArticles(self, sentence):
        #This function removes the articles that are used for grammar purpose but serve no big part in meaning purposes
        #They are removed to avoid sentence matching based on meaningless articles
        #TODO after evaluation check if it necessary to remove more particles
        #TODO check if this particles can be used somewhere else
        particles = ["the","a","of","in"]
        for word in sentence:
            if word in particles:
                sentence.remove(word)
        return sentence

    def lemmatizeWords(self, sentence):
        #lemmatizes the sentence
        lemmatized_words = []
        for word in sentence:
            new_word = wordnet_lemmatizer.lemmatize(word,pos = "v")
            lemmatized_words.append(new_word)
        return lemmatized_words


