from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import re
wordnet_lemmatizer = WordNetLemmatizer()

from nltk import download
download('stopwords')  # Download stopwords list.
#stopwords list
stop_words = stopwords.words('english')

def questionPreprocessing(question):
    #remove question mark
    question=re.sub("\?","",question)
    #lowercase and list of words
    question=question.lower().split()
    #remove useless words 
    #TODO: stop_words remove verbs, it should not
    #question=[w for w in question if w not in stop_words]
    #lemmatize
    questionLemmatized=[]
    for word in question:
        questionLemmatized.append(wordnet_lemmatizer.lemmatize(word,pos = "v"))
    
    print('Question before lemmatization', question)
    print('Question after lemmatization', questionLemmatized)
    return questionLemmatized

if __name__ == "__main__":
    questionsList=["What is a neuron?", "what is the role of the hippocampus in episodic memory?"]
    for q in questionsList:
        question=questionPreprocessing(q)