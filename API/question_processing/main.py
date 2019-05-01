from question_processing.answer import Answer
import os
import time
import pickle 

import question_processing.sentenceProcessing as sentPros

def process(question):
    start=time.time()

    #locate the dataset files
    if (os.getcwd()=="/app"):
        #app deployed
        print('using deployed path')
        path=os.getcwd()+"/data"
    else:
        #debugging app locally
        path="data"
    
    #Import the dataset with the sentences preprocessed
    with open(path+'/dataset_original', 'rb') as f:
        dataset_original = pickle.load(f)

    #Import the dataset with the sentences preprocessed
    with open(path+'/dataset_preprocessed', 'rb') as f:
        dataset_preprocessed = pickle.load(f)

    question=sentPros.removeSpecialCharacters(question)
    question=sentPros.preprocessing(question)

    #Setting up the search
    required_answer = Answer()
    required_answer.setQuestion(question)

    #Compare question-sentences and return best 3 answers
    result=required_answer.calculateTopSentences(dataset_original, dataset_preprocessed)

    print(question)
    print(result)

    end=time.time()
    print('Time required:', end-start)
    return result