from flask import Flask, render_template, redirect, flash,request, url_for
import pandas as pd
from flask_bootstrap import Bootstrap
# import openpyxl

app = Flask(__name__)
Bootstrap(app)
data = pd.read_excel('static/AWS_exam.xlsx',engine='openpyxl')
df = pd.DataFrame(data,columns=['Question', "Answer Option 1", "Answer Option 2", "Answer Option 3", "Answer Option 4","Correct Response"])
app.secret_key = 'adsfdsafasd'
answers = 0
@app.route('/')
def home():
    global answers
    answers = 0
    return render_template('index.html')


@app.route('/summary/<int:count>')
def summary(count):
    score = (count)*10
    print('---------------------------------------')

    return render_template('summary.html', score= score)
@app.route('/question/<int:ques>', methods=['POST','GET'])
def start(ques):
    global answers
    if request.method == "POST":
        if ques>=10:
            print('----------------------------------------')
            return redirect(url_for("summary", count = answers))
        chosen_a = [i for i,a in request.form.items()]
        print("chosen =",chosen_a)

        dfq = df.iloc[ques][0]
        dfo = {i+1:v for i,v in enumerate(df.iloc[ques][1:5])}
        prev_dfa = df.iloc[ques-1][5]
        if type(prev_dfa) == str:
            prev_dfa = prev_dfa.split(",")
        else:
            prev_dfa = [str(prev_dfa)]
        print("correct =",prev_dfa)
        if chosen_a == prev_dfa:
            answers += 1
            print("You are correct")
            flash("That was Correct!")
        dfa = df.iloc[ques][5]
        return render_template('test_question.html', question=dfq, options=dfo, answer=dfa, num = ques, count = answers)

    else:
        dfq = df.iloc[ques][0]
        dfo = {i+1: v for i, v in enumerate(df.iloc[ques][1:5])}
        print(dfo)
        dfa = df.iloc[ques][5]
        return render_template('test_question.html', question=dfq, options=dfo, answer=dfa, num=ques)



if __name__ == "__main__":
    app.run(debug=True)