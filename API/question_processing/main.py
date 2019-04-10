from question_processing.question import Question
from question_processing.text import Information
from question_processing.answer import Answer
import os
import time

import nltk
nltk.download('wordnet')
nltk.download('punkt')

def process(question):
    #start=time.time()
    comparison_question = Question().poseQuestion(question)

    #Setting up the search
    required_answer = Answer()
    required_answer.setQuestion(comparison_question)

    if (os.getcwd()=="/app"):
        #app deployed
        print('using deployed path')
        path=os.getcwd()+"/data"
    else:
        #debugging app locally
        path="../data"
    for file in os.listdir(path):
        try:
            currentFile = open(os.path.join(path,file),"r")
            print("File: ", file, " was successfully opened!\n")
            currentText = Information(currentFile.read())
            currentText.prepareCompare()
            required_answer.calculateTopSentences(currentText.complete_list, currentText.useful_list)
            currentFile.close()
            print("File: ", file ," was successfully closed!\n")
        except(UnicodeDecodeError):
            print("File: ", file, " is in chinese! Please check\n")
    #end=time.time()
    #print('Time required:', end-start)
    result=required_answer.getFinalAnswer()
    print(result)
    return result
