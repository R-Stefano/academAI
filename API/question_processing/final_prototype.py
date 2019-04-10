import file_iterator
from question import Question
from text import Information
from answer import Answer
import time

#Getting the user question
user_question = Question()
comparison_question = user_question.poseQuestion()

start=time.time()

#Listing all the sources for the information
sources_list = file_iterator.Source()

#Setting up the search
required_answer = Answer()
required_answer.setQuestion(comparison_question)

for file in sources_list.getSources():
    try:
        currentFile = open(file,"r")
        print("File: ", file, " was successfully opened!\n")
        currentText = Information(currentFile.read())
        currentText.prepareCompare()
        comparison_text = currentText.getUsefulText()
        required_answer.calculateTopSentences(comparison_text)
        currentFile.close()
        print("File: ", file ," was successfully closed!\n")
    except(UnicodeDecodeError):
        print("File: ", file, " is in chinese! Please check\n")
    except(FileNotFoundError):
        print("Reached the sleeping file... Dont make too much noise...\n")
end=time.time()
print('Time required:', end-start)
print(required_answer.getFinalAnswer())
