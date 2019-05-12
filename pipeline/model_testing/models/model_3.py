'''
This model extracts the most useful words from the question.
How most useful are defined?

Then it iterates through each sentence and compute the question-sentence relevance
The relevance is computed as the number of times the question-words appear in the sentence
'''
import os
import nltk
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

import tensorflow as tf
import tensorflow_hub as hub

class Model():
    def __init__(self):
        self.name="Universal_Sentence_Encoder"
        self.sess=tf.Session()

        self.modelFilePath="google_USE/"
        if(os.path.isfile(self.modelFilePath+"tfhub_module.pb")):
            print('Loading file..')
            self.model = hub.Module(self.modelFilePath)
        else:
            print('Creating model..')
            self.setup()
        
        self.sess.run([tf.global_variables_initializer(), tf.tables_initializer()])

    
    def setup(self):
        #@param "https://tfhub.dev/google/universal-sentence-encoder-large/3"
        module_url = "https://tfhub.dev/google/universal-sentence-encoder/2"

        # Import the Universal Sentence Encoder's TF Hub module
        self.model = hub.Module(module_url)

    def sentenceProcessing(self, sentence):
        #encoding sentences
        s_vecs=np.array(self.sess.run(self.model(sentence)))
        return s_vecs
    def cosineSimilarity(self, vector1, vector2):
        return np.dot(vector1, np.transpose(vector2))[0]/(np.linalg.norm(np.repeat(vector1, axis=0, repeats=vector2.shape[0]), axis=-1)*np.linalg.norm(vector2, axis=-1))
    
    def sortResults(self, top_scores, top_sentences, score, original_text):
        for idx, value in enumerate(top_scores):
            if (score >= value):
                top_scores[idx+1:]=top_scores[idx:len(top_scores)-1]
                top_scores[idx]=score
                top_sentences[idx+1:]=top_sentences[idx:len(top_sentences)-1]
                top_sentences[idx]=original_text
                break
        return top_scores, top_sentences

    def getAnswer(self, question, s_vecs, sentences):
        '''
        question: the question as a string
        sentences: a list of sentences as strings

        Return:
            top_scores: a list of integers. The score of the best 3 sentences
            top_sentences: a list of strings. The sentences with the best score
        '''
        #encoding question
        q_vec=np.array(self.sess.run(self.model([question])))[0]

        scores=cosine_similarity(np.reshape(q_vec, (1,-1)), s_vecs).tolist()
        
        top_scores=[0,0,0]
        top_sentences=["","",""]

        for idx, score in enumerate(scores):
            top_scores, top_sentences=self.sortResults(top_scores, top_sentences, score, sentences[idx])

        return top_scores, top_sentences


