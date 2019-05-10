import re
import nltk
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
# Import and download stopwords from NLTK.

def removeParenthesis(data):
    #Remove text between parehtesis
    formattedData=re.sub(r" ?\([^)]+\)", "", data)
    #Remove text that comes before ) or after (
    formattedData=re.sub('(\(.+|.+\))','',formattedData)
    return formattedData

def removeSpecialCharacters(data):
    #substitute all the characters that are not letters, numbers, white space, %, or dots with a space
    return re.sub(r'[^a-zA-Z0-9\s%\.\-]','',data)

def removeDoubleSpaces(data):
    return re.sub(" +"," ", data)
    
def preprocessing(sentence):
    #everything lower case
    sentence = sentence.lower()
    #each sentence is split in a list of words
    sentence=nltk.word_tokenize(sentence)
    #the stopwords are removed from the list of words
    particles = ["the","a","of","in","and"]
    for word in sentence:
        if word in particles:
            sentence.remove(word)
    #lemmatize the sentence
    lemmatizedSentence=[]
    for w in sentence:
        lemmatizedSentence.append(wordnet_lemmatizer.lemmatize(w,pos = "v"))

    return lemmatizedSentence


def textToLemmatized(sentences_text):
    text=removeParenthesis(sentences_text)
    text=removeSpecialCharacters(text)
    text=removeDoubleSpaces(text)
    sentencesList=text.split('.')
    formattedSentencesList=[]
    for idx, sentence in enumerate(sentencesList):
        lemmatizedSentence=preprocessing(sentence)
        formattedSentencesList.append(lemmatizedSentence)
    
    return sentencesList, formattedSentencesList

def questionPreprocessing(question_text):
    q=removeSpecialCharacters(question_text)
    q=preprocessing(q)
    return q
