'''
This file is used to setup new model versions.
The model is seen how it perform on the dataset and the results are saved for further analysis.
'''
import json
import nltk
import pickle

import analyze_embeddings as analyze

from models import model_3
model=model_3.Model()

#path to the dataset file
pathDataset="../preprocessing/test_dataset.json"

if __name__ == "__main__":
    #import the dataset
    questionsList=[]
    sentencesDataset=[]
    labelsList=[]
    with open(pathDataset) as json_file:  
        data = json.load(json_file)
        for QA in data:
            questionsList.append(QA['question'])
            #The answers comes in a single string of sentences. 
            #Create a single list of sentences
            tokenizedSentence=nltk.sent_tokenize(QA['answer'])
            sentencesDataset.extend(tokenizedSentence)
            labelsList.append(tokenizedSentence)
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
        top_scores, top_sentences=model.getAnswer(q, sentencesDataset)
        for idx, score in enumerate(top_scores):
            print('Score: {}, Sentence: {}'.format(score, top_sentences[idx]))
        
        labels_scores, _ =model.getAnswer(q, labelsList[q_idx])
        modelResults['questions'].append(q)
        modelResults['predictions']['scores'].append(top_scores)
        modelResults['predictions']['sentences'].append(top_sentences)
        modelResults['labels']['scores'].append(labels_scores)
        modelResults['labels']['sentences'].append(labelsList[q_idx])

        print('--------\n')
    
    #save results on disk
    with open(model.name+"_results", "wb") as f:
        pickle.dump(modelResults, f)