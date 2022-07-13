from flask import Flask, render_template, redirect, flash, request, url_for
import pandas as pd
from flask_bootstrap import Bootstrap
import os
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
Bootstrap(app)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    def __repr__(self):
        return '<User %r>' % self.username

db.create_all()

score = Score(score=0)
db.session.add(score)
db.session.commit()

# data = load_workbook(filename= 'static/AWS_exam.xlsx')

# open sheet
data = pd.read_excel('static/AWS_exam.xls')

# data-frame of the excel sheet
df = pd.DataFrame(data,columns=['Question', "Answer Option 1", "Answer Option 2", "Answer Option 3", "Answer Option 4","Correct Response"])

# ++++ Set ENV varaiable when hosting on server. Don't keep it open like this ++++++
os.environ['SECRET_KEY'] = 'adsfdsafasd'
app.secret_key = os.getenv('SECRET_KEY')


# starting landing-page
@app.route('/')
def home():
    current_score = Score.query.get(1)
    current_score.score = 0
    db.session.commit()
    print('score is reset')
    print(current_score.score)
    return render_template('index.html')


# final summary page
@app.route('/summary/<int:count>')
def summary(count):
    score = (count)*10

    return render_template('summary.html', score= score)

# each question's page (dynamically made for each question)
@app.route('/question/<int:ques>', methods=['POST','GET'])
def start(ques):
    
    current_score = Score.query.get(1)
    print('score so far is: ',current_score.score)

    # if an answer has been sent (i.e this is second question or more)
    if request.method == "POST":
        if ques>=10:
            print('----------------------------------------')
            return redirect(url_for("summary", count = current_score.score))
        
        # the chosen answers (the ones sent from the previous page)
        chosen_a = [i for i,a in request.form.items()]
        print("chosen =",chosen_a)
        print(chosen_a)

        # question text content
        dfq = df.iloc[ques][0]

        # possible options
        dfo = {i+1:v for i,v in enumerate(df.iloc[ques][1:5])}

        # previous question's answer (e.g 1, 2, 3, 4). This is to check if our submitted answer is correct (to be displayed on the next page)
        prev_dfa = df.iloc[ques-1][5]

        # if there are two answers (like "1,2") then prev_dfa is sent as a string, which we need to account for.
        # We need to split the string and make it a list
        if type(prev_dfa) == str:
            prev_dfa = prev_dfa.split(",")
    
        # if it is a single answer ( like "1") ,then it formats the answers as a string and in a list (to match the above)
        else:
            prev_dfa = [str(prev_dfa)]
        print("The correct answer is:", prev_dfa)

        # check if your answers are correct
        if chosen_a == prev_dfa:
            current_score.score += 1
            print(current_score.score)
            db.session.commit()
            print("You are correct")
            flash("That was Correct!")

        # current question's answer (to be sent to the next page)
        dfa = df.iloc[ques][5]
        return render_template('test_question.html', question=dfq, options=dfo, answer=dfa, num = ques, count = current_score.score)
    
    # if it is the first question in the test
    else:
        dfq = df.iloc[ques][0]
        dfo = {i+1: v for i, v in enumerate(df.iloc[ques][1:5])}
        dfa = df.iloc[ques][5]
        return render_template('test_question.html', question=dfq, options=dfo, answer=dfa, num=ques)



if __name__ == "__main__":
    app.run(debug=True)
