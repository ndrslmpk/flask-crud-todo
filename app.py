import string
from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/todoapp'
db = SQLAlchemy(app)

# models
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)

  def __repr__(self):
      return f'<Todo {self.id} {self.description}>'

db.create_all()

@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())

@app.route('/add')
def add():
   if request.method == 'POST':
      results = request.form
      session.add(Todo(description = results.description))