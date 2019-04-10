#This file contains the class "Answer"
#The purpose of the class is to compare the lemmatized question with the lemmatized text
#This was done like this because it avoids redundancy in variables and simplifies code

class Answer:
    top_sentence = ""
    second_sentence = ""
    third_sentence = ""
    top_similarity = 0
    second_similarity = 0
    third_similarity = 0
    final_answer = ["","",""]
    question = []


    def setQuestion(self,question):
        self.question = question
        print(self.question)
        
    def calculateTopSentences(self,text):
        #This function determines which sentences are the top ranked
        for sentence in text:
            sentence_similarity = self.getSimilarityIndex(sentence)
            if (sentence_similarity > self.third_similarity):
                #If the sentence_similarity is higher than the third most similar phrase
                if(sentence_similarity >= self.second_similarity):
                    #If the sentence_similarity is higher than the second most similar phrase
                    if(sentence_similarity >= self.top_similarity):
                        #If the sentence_similarity is higher than the top similar sentence
                        #You have to shift everything downwards before touching the upper one
                        self.third_similarity = self.second_similarity
                        self.third_sentence = self.second_sentence
                        self.second_similarity = self.top_similarity
                        self.second_sentence = self.top_sentence
                        #Actually changing the upper one
                        self.top_similarity = sentence_similarity
                        self.top_sentence = sentence
                    else:
                        #If the sentence_similarity is higher than the second and third one, but not the top one
                        self.third_similarity = self.second_similarity
                        self.third_sentence = self.second_sentence
                        self.second_similarity = sentence_similarity
                        self.second_sentence = sentence
                else:
                    #If the sentence_similarity is higher than the third one only
                    self.third_similarity = sentence_similarity
                    self.third_sentence = sentence                        
        
            
    def getSimilarityIndex(self,sentence):
        #This function calculates how much a sentence resembles the question
        try:
            counter = 0
            similarity = 0
            for word in self.question:
                if word in sentence:
                    counter = counter + 1
                else:
                    counter = counter
            similarity = counter + (counter/len(sentence))
        except ZeroDivisionError:
            print("There is an issue here!")
            similarity = 0
        return similarity

    def getFinalAnswer(self):
        self.final_answer = [self.top_sentence, self.second_sentence, self.third_sentence]
        return self.final_answer
