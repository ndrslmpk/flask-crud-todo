from email.policy import default
import string
import sys
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from itsdangerous import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=True)

  def __repr__(self):
      return f'<Todo {self.id} {self.description}>'


@app.route('/')
def index():
  return render_template('index.html', data=Todo.query.all())

@app.route('/create', methods=['POST'])
def create():
  error = False
  body = {}
  try:
    _description = request.get_json()['description'] # returns a dictionary 
    _todo = Todo(description = _description)
    db.session.add(_todo)
    db.session.commit()
    body['description'] = _todo.description 
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return jsonify(body)

@app.route('/<int:_id>', methods=['POST'])
def update():
  error = False
  body = {}
  try:
    print(request.get_json()['id'])
    _id= request.get_json()['id']
    _todo = Todo.query.get(_id)
    if request.get_json()['description'] != None:
      _todo.description = request.get_json()['description']
      body['description'] = _todo.description
    if request.get_json()['completed'] != None:
      _todo.completed = request.get_json()['completed']
      body['completed'] = _todo.completed
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  else:
    return jsonify(body)


@app.route('/delete', methods=['DELETE'])
def delete():
  error = False
  body = {}