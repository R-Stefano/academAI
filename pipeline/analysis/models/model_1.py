'''
This model extracts the most useful words from the question.
How most useful are defined?

Then it iterates through each sentence and compute the question-sentence relevance
The relevance is computed as the number of times the question-words appear in the sentence
'''
import nltk
import re
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class Model():
    def __init__(self):
        self.name="rule-based"
        self.q_stop_words=["what","a","the"]
        self.wordnet_lemmatizer = WordNetLemmatizer()
    
    def questionPreprocessing(self, question):
        '''
        question: the question as a string

        Return:
            q: a list of tuples such as [('be', 'VB'), ('motor', 'NN'), ('neuron', 'NN')]
        '''
        q=question.lower()
        #substitute all the characters that are not letters, numbers, white space, %, or dots with a space
        q=re.sub(r'[^a-zA-Z0-9\s%\-]','',q)
        q=nltk.word_tokenize(q)

        #lemmatize question
        lemmatizedQuestion=[]
        for w in q:
            lemmatizedQuestion.append(self.wordnet_lemmatizer.lemmatize(w,pos = "v"))

        q=[w for w in lemmatizedQuestion if w not in self.q_stop_words]

        q=nltk.pos_tag(q)
        return q
    
    def sentenceProcessing(self, sentence):
        '''
        sentence: a sentence as a string

        Return:
            lemmatizedSentence: a list of words. Each word has been processed
        '''
        s=sentence.lower()
        s=re.sub(r'[^a-zA-Z0-9\s%\-]','',s)
        s=nltk.word_tokenize(s)
        lemmatizedSentence=[]
        for w in s:
            lemmatizedSentence.append(self.wordnet_lemmatizer.lemmatize(w,pos = "v"))
        return lemmatizedSentence

    def computeSimilarity(self, q, s):
        '''
        q: list of tuples such as [('be', 'VB'), ('motor', 'NN'), ('neuron', 'NN')]
        s: list of words 
        '''
        scores={}        
        stop_tags=["VB", "IN"] #which tags to weight less
        
        for w_q,w_tag in q:
            scores[w_q]={'value':0, 'count':1}

            #weight less stop words in the question
            if w_tag in stop_tags:
                weight=0.5
            else: 
                weight=1.0

            for idx, w_s in enumerate(s):
                weight_position=(len(s)-idx)/len(s)
                if w_s==w_q:
                    scores[w_q]['value'] += (weight*1) * weight_position
                    scores[w_q]['count'] += 1
        tot_score=0
        for key in scores:
            tot_score += scores[key]['value']/scores[key]['count']**2
        return tot_score
    
    def sortResults(self, top_scores, top_sentences, score, original_text):
        for idx, value in enumerate(top_scores):
            if (score >= value):
                top_scores[idx+1:]=top_scores[idx:len(top_scores)-1]
                top_scores[idx]=score
                top_sentences[idx+1:]=top_sentences[idx:len(top_sentences)-1]
                top_sentences[idx]=original_text
                break
        return top_scores, top_sentences

    def getAnswer(self, question, sentences):
        '''
        question: the question as a string
        sentences: a list of sentences as strings

        Return:
            top_scores: a list of integers. The score of the best 3 sentences
            top_sentences: a list of strings. The sentences with the best score
        '''
        q=self.questionPreprocessing(question)

        top_scores=[0,0,0]
        top_sentences=["","",""]

        for sentence in sentences:
            score=self.computeSimilarity(q, self.sentenceProcessing(sentence))
            top_scores, top_sentences=self.sortResults(top_scores, top_sentences, score, sentence)

        return top_scores, top_sentences
        


