'''
This file loads the results in the results's folder for different models for comparing how they performed
'''
import os
import pickle
import numpy as np
import json

import matplotlib.pyplot as plt


folderResults="results_data"
imagesFolder="imgs"

def assessScore(model, labelSentencesList, predSentencesList):
    print('Computing average WMDistance between label sentences and predicted sentence')
    scores=[]
    for labelSentence in labelSentencesList:
        for predSentence in predSentencesList:
            if len(labelSentence)>0:
                scores.append(model.model.wmdistance(labelSentence, predSentence))
    print('Word Mover distance (lower better): {:.2f}'.format(np.mean(scores)))

def accuracy(modelsResults):
    '''
    AT the moment we are interested that one of the correct answers in showed in the top 3 results.
    IN order to be evaluated by the users and have a constant growinw dataset for later one supervised learning.

    So, the model's accuracy is evaluated based on if a correct sentence appears in the top 3 results.
    '''
    ModelsWrongPredsIdxs={}
    ModelsAccuracies={}
    for modelResult in modelsResults:
        print('Model:', modelResult['name'])
        modelAccuracy=[]
        #check if one of the predicted sentences is in the label sentences list
        for exampleIdx, exampleSent in enumerate(modelResult['predictions']['sentences']):
            found=False
            for s in exampleSent:
                if (s in modelResult['labels']['sentences'][exampleIdx]):
                    found=True
            modelAccuracy.append(found)

        ModelsWrongPredsIdxs[modelResult['name']]=np.argwhere(np.asarray(modelAccuracy)==False)
        
        ModelsAccuracies[modelResult['name']]=np.mean(modelAccuracy)
    
    for idx, key in enumerate(ModelsAccuracies):
        plt.bar(idx+1, ModelsAccuracies[key], label=key)
        plt.text(idx+0.9, ModelsAccuracies[key]+0.01, '{:.2f}'.format(ModelsAccuracies[key]) ,color='black', fontweight='bold')
    
    plt.xticks([i+1 for i in range(len(ModelsAccuracies))], [key for key in ModelsAccuracies], rotation=45)
    plt.show()
    return ModelsWrongPredsIdxs

def displayWrongPreds(ModelsWrongPredsIdxs, modelsResults):
    #questions=np.asarray(models_results['questions'])
    #labelSentences=np.asarray(models_results['labelSentences'])
    for modelResult in modelsResults:
        print('Display wrong predictions for', modelResult['name'])
        idxs=ModelsWrongPredsIdxs[modelResult['name']]

        #Retrieve the data of wrong predictions to display
        wrongQues=np.asarray(modelResult['questions'])[idxs].tolist()
        wrongPreds=np.asarray(modelResult['predictions']['sentences'])[idxs].tolist()
        wrongPredsScores=np.asarray(modelResult['predictions']['scores'])[idxs].tolist()
        wrongPredsTruesSent=np.asarray(modelResult['labels']['sentences'])[idxs].tolist()
        wrongPredsTruesSentScores=np.asarray(modelResult['labels']['scores'])[idxs].tolist()

        #display each wrong prediction
        img_idx=0
        for q, pred, predScore, trueSent, trueSentScore in zip(wrongQues, wrongPreds, wrongPredsScores, wrongPredsTruesSent, wrongPredsTruesSentScores):
            #remove double list
            predScore=predScore[0]
            trueSentScore=trueSentScore[0]
            pred=pred[0]
            trueSent=trueSent[0]
            print('Question:', q[0])
            for idx, p in enumerate(pred):
                print('Score: {:.2f} | {}'.format(predScore[idx], p))
            print('\nLabels')
            for idx, p in enumerate(trueSent):
                print('Score: {:.2f} | {}'.format(trueSentScore[idx], p))
            print('\n--------------\n')
            #define y-axis values
            yaxis=[i for i in range(len(predScore) + len(trueSentScore))]

            #define x-axis value center for each bar 
            plt.barh(yaxis[:len(predScore)],predScore, color='red', label='preds')
            plt.barh(yaxis[len(predScore):],trueSentScore, color='green', label='trues')  

            #display bar-height (score) on top of the bar
            for i, v in enumerate(predScore + trueSentScore):
                plt.text(v+0.005, i-0.1, '{:.4f}'.format(v) , color='black', fontweight='bold')

            #Split the y tick texts on multiple lines. The sentences are too long
            splittedTextYTicks=[]
            for y_tick_text in (pred+trueSent):
                multiLines=""
                c_count=0
                for i, w in enumerate(y_tick_text.split()):
                    c_count+=len(w)
                    multiLines+=w+" "
                    if (c_count>35):
                        c_count=0
                        multiLines+="\n"
                if len(multiLines)>200:
                    multiLines[:200]
                splittedTextYTicks.append(multiLines)

            plt.yticks(yaxis, splittedTextYTicks)

            plt.xlabel('Similarity Score')
            plt.xticks([])
            plt.title(q[0])
            plt.legend(loc=0)
            mng = plt.get_current_fig_manager()
            mng.full_screen_toggle()
            plt.tight_layout()
            plt.savefig(imagesFolder+'/{}_q{}.png'.format(modelResult['name'], img_idx))
            #plt.show()
            img_idx +=1
        print('\n\n-----------------\n\n')
modelsResults=[]
for filename in os.listdir(folderResults):
    modelResult=pickle.load(open(os.path.join(folderResults,filename), "rb"))

    modelsResults.append(modelResult)

ModelsWrongPredsIdxs=accuracy(modelsResults)
displayWrongPreds(ModelsWrongPredsIdxs, modelsResults)