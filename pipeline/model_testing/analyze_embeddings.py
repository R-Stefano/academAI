'''
This file is used to provide the tools to analyze model versions.
The analysis should tells if the model created meaningful embeddings
'''
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
import numpy as np

def computeWMD(model, sentences1, sentences2):
    print('Computing Word Mover Distance (Low score means more similar)')
    if len(sentences1)!=len(sentences2):
        isTargetSentence=True
        s=sentences1[0]
        for i in range(len(sentences2)-1):
            sentences1.append(s)
    else:
        isTargetSentence=False

    inputS1=[]
    inputS2=[]
    for idx, sentence in enumerate(sentences2):
        inputS1.append(model.sentenceProcessing(sentences1[idx]))
        inputS2.append(model.sentenceProcessing(sentence))

    scores=[]
    for s1,s2 in zip(inputS1,inputS2):

        scores.append(model.model.wmdistance(s1,s2))
    
    if isTargetSentence:
        print(sentences1[0])
        print(sentences2[np.argmin(scores)])
        print('Score:', np.min(scores))
        print('--------')

def displayEmbeddings(X, words):
    print('Showing embeddings of words..')
    #initialize model
    tsne_model = TSNE(perplexity=1, n_components=2, init="pca", n_iter=5000, random_state=23)
    Y = tsne_model.fit_transform(X)

    fig, ax = plt.subplots(figsize=(20,10))
    ax.scatter(Y[:, 0], Y[:, 1])
    words = list(words)
    for i, word in enumerate(words):
        plt.annotate(word, xy=(Y[i, 0], Y[i, 1]))

    ax.set_yticklabels([]) #Hide ticks
    ax.set_xticklabels([]) #Hide ticks
    plt.show()

def similarWords(model, wordsList):
    print('Showing most similar words..')
    for w in wordsList:
        print("{} -> {}: {:.4f}".format(w, *model.similar_by_word(w)[0]))