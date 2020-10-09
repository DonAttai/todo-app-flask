from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return f"Todo('{self.title}')"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        todo_title = request.form['title']
        new_todo = Todo(title=todo_title)

        try:
            db.session.add(new_todo)
            db.session.commit()
            return redirect('/')
        
        except:
            return "couldn't add todo item"
    else:
        todos = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', todos=todos)


@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    todo = Todo.query.get_or_404(id)

    if request.method == 'POST':
        todo.title = request.form['title']

        try:
            db.session.commit()
            return redirect('/')
        
        except:
            return "couldn't update todo item, there was a problem"



    else:
        return render_template('update.html', todo=todo)

   




@app.route('/delete/<int:id>')
def delete(id):
    todo = Todo.query.get_or_404(id)

    try:
        db.session.delete(todo)
        db.session.commit()
        return redirect('/')
    except:
        return "Couldn't delete todo item, there was a problem"


