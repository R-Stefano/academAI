'''
This file is used to setup new model versions.
The model is seen how it perform on the dataset and the results are saved for further analysis.
'''
import json
import nltk
import pickle
import os
import analyze_embeddings as analyze

from models import model_3 as mdl
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
    processedLabels=[]
    for example in labelsList:
        ex_list=[]
        for s in example:
            ex_list.append(model.sentenceProcessing(s))
        processedLabels.append(ex_list)
    
    return processedLabels

if __name__ == "__main__":
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
            #process each sentence according to the model
            for i, s in enumerate(datasetTokenized):
                print(i)
                sentencesDataset.append(model.sentenceProcessing(s))

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
    '''
    '''
    vecs2d=[]
    #work on lower dimensional vectors(2) and not 300
    for s in sentencesDataset:
        s=model.sentenceProcessing(s)
        vecs2d.extend(model.model[s])
    
    print(len(vecs2d))
    '''

    modelResults={
        'name':model.name,
        'questions': [],
        'predictions': {'scores':[], 'sentences':[]},
        'labels': {'scores':[], 'sentences':[]}
        }

    for q_idx, q in enumerate(questionsList):
        print('Question', q)
        top_scores, top_sentences=model.getAnswer(q, sentencesDataset, datasetTokenized)
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
    
    #save model_dataset on disk
    with open(model.name+"_original_data", "wb") as f:
        pickle.dump(datasetTokenized, f)

    with open(model.name+"_processed_data", "wb") as f:
        pickle.dump(sentencesDataset, f)