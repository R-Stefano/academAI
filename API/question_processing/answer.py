#This file contains the class "Answer"
#The purpose of the class is to compare the lemmatized question with the lemmatized text
#This was done like this because it avoids redundancy in variables and simplifies code

class Answer:
    top_similarities = [0,0,0]
    top_sentences = ["","",""]

    def setQuestion(self,question):
        self.question = question         

    def calculateTopSentences(self,original_text, processed_text):
        #This function determines which sentences are the top ranked
        for s_idx, sentence in enumerate(processed_text):
            sentence_similarity = self.getSimilarityIndex(sentence)
            for idx, value in enumerate(self.top_similarities):
                if (sentence_similarity >= value):
                    self.top_similarities[idx+1:]=self.top_similarities[idx:len(self.top_similarities)-1]
                    self.top_similarities[idx]=sentence_similarity
                    self.top_sentences[idx+1:]=self.top_sentences[idx:len(self.top_sentences)-1]
                    self.top_sentences[idx]=original_text[s_idx]
                    break

    def getSimilarityIndex(self,sentence):
        #This function calculates how much a sentence resembles the question
        try:
            counter = 0
            similarity = 0
            for word in self.question:
                if word in sentence:
                    counter = counter + 1
            similarity = counter + (counter/len(sentence))
        except ZeroDivisionError:
            print("The length of the sentence is 0")
            similarity = 0
        return similarity

    def getFinalAnswer(self):
        return self.top_sentences
