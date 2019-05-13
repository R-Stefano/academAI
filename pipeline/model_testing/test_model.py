'''
This file is used to setup new model versions.
The model is seen how it perform on the dataset and the results are saved for further analysis.
'''
import json
import nltk
import pickle
import os
import numpy as np
import analyze_embeddings as analyze
from sklearn.decomposition import TruncatedSVD
from model import model_3 as mdl
import matplotlib.pyplot as plt
import pandas as pd 


#path to the dataset file
pathDataset="../preprocessing/test_dataset.json"
datasetPath="dataset.txt"

def loadQuestions():
    #import the dataset
    questionsList=[]
    labelsList=[]
    with open(pathDataset) as json_file:  
        data = json.load(json_file)
        for QA in data:
            questionsList.append(QA['question'])
            #The answers comes in a single string of sentences. 
            #Create a single list of sentences
            tokenizedSentence=nltk.sent_tokenize(QA['answer'])
            labelsList.append(tokenizedSentence)
    
    return questionsList, labelsList

def processTestSentences(labelsList, model):
    processedLabels=[]
    for example in labelsList:
        ex_list=[]
        for s in example:
            ex_list.append(model.sentenceProcessing(s))
        processedLabels.append(ex_list)
    
    return processedLabels

if __name__ == "__main__":
    model=mdl.Model()
    textSentences, processedSentences=model.setupData("dataset.csv")

    print('original dataset', len(textSentences))
    print('processed dataset', len(processedSentences))
    
    #import test sentences
    questionsList, labelsList=loadQuestions()

    #process test sentences
    processedLabels=processTestSentences(labelsList, model)

    '''
    #analyze embeddings
    analyze.similarWords(model.model, ["neuron","hippocampus","neocortex","memory"])

    x=[]
    words=[]
    sentences=[sentencesDataset[0], sentencesDataset[3], sentencesDataset[32]]
    for s in sentences:
        s=model.sentenceProcessing(s)
        x.extend(model.model[s])
        words.extend(s)

    analyze.displayEmbeddings(x, words)
    analyze.computeWMD(model, [sentencesDataset[0]], sentencesDataset[1:])
    #Explore best n_components in PCA
    vecs=[]
    #work on lower dimensional vectors(2) and not 300
    for s in sentencesDataset:
        vecs.extend(s)

    del sentencesDataset
    del model
    print(np.asarray(vecs[:100000]).shape)
    pca=IncrementalPCA().fit(vecs)
    plt.figure()
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.show()
    '''
    
    modelResults={
        'name':model.name,
        'questions': [],
        'predictions': {'scores':[], 'sentences':[]},
        'labels': {'scores':[], 'sentences':[]}
        }

    for q_idx, q in enumerate(questionsList):
        print('Question', q)
        top_scores, top_sentences=model.getAnswer(q, processedSentences, textSentences)
        for idx, score in enumerate(top_scores):
            print('Score: {}, Sentence: {}'.format(score, top_sentences[idx]))
        
        labels_scores, _ =model.getAnswer(q, processedLabels[q_idx], labelsList[q_idx])
        modelResults['questions'].append(q)
        modelResults['predictions']['scores'].append(top_scores)
        modelResults['predictions']['sentences'].append(top_sentences)
        modelResults['labels']['scores'].append(labels_scores)
        modelResults['labels']['sentences'].append(labelsList[q_idx])

        print('--------\n')
    #save results on disk
    with open(model.name+"_results", "wb") as f:
        pickle.dump(modelResults, f)

