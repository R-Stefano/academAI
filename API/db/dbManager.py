from flask_sqlalchemy import SQLAlchemy

#init DB object
db = SQLAlchemy()

class QueryEntry(db.Model):
    '''
    The table Queries stores the questions
    and assign an id to it
    '''
    __tablename__ = 'queries'

    id = db.Column(db.Integer, primary_key=True)
    questions = db.Column(db.String(256))

    def __init__(self,question):
        self.questions = question

class AnswerEntry(db.Model):
    '''
    The table answers stores the answers
    assigned to the question id and the rating id
    '''
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)
    query_id=db.Column(db.Integer)
    answer = db.Column(db.String(256))
    rating_id=db.Column(db.Integer)

    def __init__(self,query_id, answer,rating):
        self.query_id=query_id
        self.answer = answer
        self.rating_id=rating