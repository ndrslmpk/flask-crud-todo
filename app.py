import string
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
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

@app.route('/create', methods=['POST'])
def create():
  _description = request.get_json()['description'] # returns a dictionary 
  _todo = Todo(description = _description)
  db.session.add(_todo)
  db.session.commit()
  return jsonify({
   'description': _todo.description
  }) 