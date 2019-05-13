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
from sklearn.decomposition import TruncatedSVD, PCA
from models import model_3 as mdl
import matplotlib.pyplot as plt

model=mdl.Model()

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
    numSentencesExample=[]
    inputModel=[]
    for example in labelsList:
        numSentencesExample.append(len(example))
        inputModel.extend(example)

    processedLabels=model.sentenceProcessing(inputModel)
    
    return processedLabels, numSentencesExample, inputModel

if __name__ == "__main__":
    '''
    #import frequencies (FOR MODEL 5)
    with open('wordsProb.json') as f:
        freqs=json.load(f)

    model=mdl.Model(freqs)
    '''
    #Import dataset
    if os.path.isfile(model.name+"_processed_data"):
        print('Loading dataset..')
        datasetTokenized=pickle.load(open(model.name+"_original_data", "rb"))
        sentencesDataset=pickle.load(open(model.name+"_processed_data", "rb"))
    else:
        print('Creating dataset..')
        sentencesDataset=[]
        with open(datasetPath) as dataset:
            data= dataset.read()
            datasetTokenized=nltk.sent_tokenize(data)
            for idx, s in enumerate(datasetTokenized):
                sentencesDataset.append(model.sentenceProcessing(s))

    '''
    #remove first common component (FOR MODEL 5)
    #1. compote common component
    X=np.asarray(sentencesDataset)
    svd = TruncatedSVD(n_components=1, n_iter=7, random_state=0)
    svd.fit(X)
    comps=svd.components_
    #2. Subtract from the sentences embeddings their projections on their first principal component. 
    #This should remove variation related to frequency and syntax that is less relevant semantically.
    sentencesDataset=X - X.dot(comps.transpose()) * comps
    '''
    #import test sentences
    questionsList, labelsList=loadQuestions()

    #process test sentences
    processedLabels, numSentencesExample, listSentencesLabels=processTestSentences(labelsList, model)
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

    #COMPONENTS VARIANCE TO REDUCE DIMENSIONALITY DATASET
    plt.figure()
    plt.plot(np.cumsum(pca.explained_variance_ratio_))
    plt.xlabel('Number of components')
    plt.ylabel('% of Variance')
    plt.show()
    '''
    modelResults={
        'name':model.name,
        'questions': [],
        'predictions': {'scores':[], 'sentences':[]},
        'labels': {'scores':[], 'sentences':[]}
        }

    q_vecs=model.getTestAnswer(questionsList)
    
    pca=PCA(n_components=250)
    sentencesDataset=pca.fit_transform(sentencesDataset)
    processedLabels=pca.transform(processedLabels)
    q_vecs=pca.transform(q_vecs)

    scores=model.computeSimilarityTest(q_vecs, sentencesDataset)
    scoresLabels=model.computeSimilarityTest(q_vecs, processedLabels)
    print('encoded questions', q_vecs.shape)
    print('scores questions-sentences', scores.shape)
    print('encoded correct sentences', processedLabels.shape)
    print('scores questions-true_sentences', scoresLabels.shape)

    c_start=0
    for q_idx, q_vec in enumerate(q_vecs):
        #prediction scores
        top_scores, top_sentences=model.getTopScoresTest(scores[q_idx], datasetTokenized)
        for idx, score in enumerate(top_scores):
            print('Score: {}, Sentence: {}'.format(score, top_sentences[idx]))
        
        #labels scores
        example_N_label_sentences=numSentencesExample[q_idx]
        c_end=c_start + example_N_label_sentences
        for i in range(example_N_label_sentences):
            top_scores_lab, top_sentences_lab=model.getTopScoresTest(scoresLabels[q_idx][c_start:c_end], listSentencesLabels[c_start:c_end])
        c_start=c_end

        modelResults['questions'].append(questionsList[q_idx])
        modelResults['predictions']['scores'].append(top_scores)
        modelResults['predictions']['sentences'].append(top_sentences)
        modelResults['labels']['scores'].append(top_scores_lab)
        modelResults['labels']['sentences'].append(top_sentences_lab)
        print('--------\n')

    #save results on disk
    with open(model.name+"_results", "wb") as f:
        pickle.dump(modelResults, f)
    '''
    #save model_dataset on disk
    with open(model.name+"_original_data", "wb") as f:
        pickle.dump(datasetTokenized, f)

    with open(model.name+"_processed_data", "wb") as f:
        pickle.dump(sentencesDataset, f)
    '''