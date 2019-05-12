'''
This model extracts the most useful words from the question.
How most useful are defined?

Then it iterates through each sentence and compute the question-sentence relevance
The relevance is computed as the number of times the question-words appear in the sentence
'''
import os
import re
import numpy as np

from flair.data import Sentence
from flair.embeddings import WordEmbeddings
from flair.models import SequenceTagger

class Model():
    def __init__(self):
        self.name="fasttext weighted_tags"
        
        modelFilePath="flair_fasttext/en-fasttext-news-300d-1M"
        if(os.path.isfile(modelFilePath)):
            print('Loading file..')
            self.model = WordEmbeddings(modelFilePath)
        else:
            print('Creating model..')
            self.setup()
    
    def setup(self):
        self.model = WordEmbeddings('news')
        self.tagger = SequenceTagger.load('pos-fast')

    def questionPreprocessing(self, question):
        '''
        question: the question as a string

        Return:
            question_obj: a Sentence object tokenized containing the question
        '''
        q=question.lower()
        #substitute all the characters that are not letters, numbers, white space, %, or dots with a space
        q=re.sub(r'[^a-zA-Z0-9\s%\-]','',q)
        question_obj=Sentence(q)

        self.model.embed(question_obj)
        self.tagger.predict(question_obj)

        dic_res=question_obj.to_dict(tag_type='pos')
        relevantTags=["NN","JJ"]

        q_vecs=[]
        #assign a weight of 1 to NN, NNS, JJ, JJS tags 0.5 to all the others
        for tag, token in zip(dic_res['entities'], question_obj):
            w=0.5
            if tag['type'][:2] in relevantTags:
                w=1.0

            q_vecs.append(token.embedding.data.numpy() * w)
                 
        return np.mean(q_vecs, axis=0)
    
    def sentenceProcessing(self, sentence):
        '''
        sentence: a sentence as a string

        Return:
            sentence_obj: a Sentence object tokenized
        '''
        s=sentence.lower()
        s=re.sub(r'[^a-zA-Z0-9\s%\-]','',s)
        sentence_obj=Sentence(s)

        #Convert words to vecs
        self.model.embed(sentence_obj)
        #Define words' tags
        self.tagger.predict(sentence_obj)
        dic_res=sentence_obj.to_dict(tag_type='pos')
        relevantTags=["NN","JJ"]
        w_vecs=[]
        #assign a weight of 1 to NN, NNS, JJ, JJS tags 0.5 to all the others
        for tag, token in zip(dic_res['entities'], sentence_obj):
            w=0.5
            if tag['type'][:2] in relevantTags:
                w=1.0
            w_vecs.append(token.embedding.data.numpy() * w)

        #average word vectors to create a "sentence" vector
        return np.mean(w_vecs, axis=0)

    def cosineSimilarity(self, vector1, vector2):
        return np.dot(vector1, vector2)/(np.linalg.norm(vector1)*np.linalg.norm(vector2))

    def computeSimilarity(self, q_vec, s_vec):
        return self.cosineSimilarity(q_vec, s_vec)
    
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
        q_vec=self.questionPreprocessing(question)

        top_scores=[0,0,0]
        top_sentences=["","",""]

        for idx, s_vec in enumerate(s_vecs):
            score=self.computeSimilarity(q_vec, s_vec)
            top_scores, top_sentences=self.sortResults(top_scores, top_sentences, score, sentences[idx])
        
        return top_scores, top_sentences
        


