from flask import Flask, render_template, request
import json
import os
import question_processing.main as q_handler
import mysql.connector
import sqlparse

model_version=0

#open connection
app = Flask(__name__)

def setConnection():
    global mydb, mycursor
    mydb = mysql.connector.connect(
        host="us-cdbr-iron-east-03.cleardb.net",
        user="be71cc213eeaba",
        passwd="57a45c0b",
        database="heroku_97435f84a55babb",
        connection_timeout=120 #keep connection open for 30 min
    )

    mycursor = mydb.cursor()
setConnection()

@app.route("/")
def home():
    '''
    This function is called when the user hits the landing page(www.academai.uk/). 
    It returns the HTML to display
    '''
    return render_template("home.html")

@app.route('/generate_text', methods=['POST'])
def generate_text():
    '''
    This function use the input/question posted by the user 
    to retrieve from the files the 5 most related sentences in order 
    to answer the question.
    This function is called when the user click generate btn.

    request.json:
        {'input': 'input_text'}
    
    '''
    if request.method == "POST":
        #Retrieve the question
        question=request.json['input']
        #this line must be changed with the processor
        sentences=q_handler.process(question) #['here the first sentence','here the second sentence.','here the third one which is a little more longer']
        #Create Json format to send back to front
        data = {
            'sentences':sentences
        }
        data = json.dumps(data)
    else:
        data='Invalid request'
    return data

@app.route('/save_db', methods=['POST'])
def save_db():
    '''
    This function save previous queries on database.
    It is called when the user is leaving the page or 
    when the user is sending a new query.

    request.json:
    {'input': 'input_text', 
     'sentences': [{'sentence': 'sentence_1', 'rating': 'positiveTag'}, 
                   {'sentence': 'sentence_2', 'rating': 'negativeTag'}, 
                   {'sentence': 'sentence_3', 'rating': 'positiveTag'}]
    }

    '''
    tag_ids={
        'negativeTag':0,
        'none':1,
        'positiveTag':2
    }
    if request.method == "POST":
        #retrieve the data sended
        data=request.json
        #connection with the db lost, reset it
        if not(mydb.is_connected()):
            setConnection()
        #Insert the question
        sql = "INSERT INTO queries (question,timestep,model_version) VALUES ('{}', NOW(), {})".format(data['input'], model_version)
        mycursor.execute(sql)
        mydb.commit()

        #retrieve the id assigned to the new entry
        q_id=mycursor.lastrowid
        for s in data['sentences']:
            try:
                sqlparse.parse(s['sentence'])
                sql = "INSERT INTO answers VALUES (0, {} ,'{}', {})".format(q_id, s['sentence'], tag_ids[s['rating']])
                mycursor.execute(sql)
            except mysql.connector.errors.ProgrammingError:
                print("Bad statement. Ignoring. \n", s['sentence'])   
        mydb.commit() 
        return 'query saved'
    else:
        return 'error while saving the query'

if __name__ == "__main__":
    app.run(debug=True)