import string
import sys
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import json

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

@app.route('/delete', methods=['DELETE'])
def delete():
  error = False
  body = {}