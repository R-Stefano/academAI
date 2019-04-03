from flask import Flask, render_template, request
import json
import os
import psycopg2

DATABASE_URL='postgres://zvooegvhaqwbne:aba6c4f9bc784483820d76ff32a1b3bb7abdc87edf95f1eeaa1ec8643aa460c4@ec2-23-23-173-30.compute-1.amazonaws.com:5432/d1p8og4frpej6q'

conn=psycopg2.connect(DATABASE_URL)
#open connection
cur = conn.cursor()
app = Flask(__name__)

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
    
    TODO: Change the sentences line in order to get the processed text
    '''
    if request.method == "POST":
        #Retrieve the question
        question=request.json['input']
        #this line must be changed with the processor
        sentences=['here the first sentence','here the second sentence.','here the third one which is a little more longer']
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

    TODO: add queries for db
    '''
    tag_ids={
        'negativeTag':0,
        'none':1,
        'positiveTag':2
    }
    if request.method == "POST":
        #retrieve the data sended
        data=request.json
        print('saving data on db')
        #Insert the question and retrieve its id to use in the following
        cur.execute("INSERT INTO d_queries(question) VALUES('{}') RETURNING id;".format(data['input']))
        q_id = cur.fetchall()[0][0]
        for s in data['sentences']:
            print(s['rating'])
            print(tag_ids[s['rating']])
            cur.execute("INSERT INTO d_answers(query_id, answer, rating) VALUES({},'{}',{});".format(q_id, s['sentence'], tag_ids[s['rating']]))
    
        return 'query saved'
    else:
        return 'error while saving the query'


if __name__ == "__main__":
    app.run(debug=True)