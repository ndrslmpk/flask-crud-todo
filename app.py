from email.policy import default
import string
import sys
from flask import Flask, abort, jsonify, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from itsdangerous import json

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app, metadata=metadata)
migrate = Migrate(app, db)

# models
class Todo(db.Model):
  __tablename__ = 'todos'
  id = db.Column(db.Integer, primary_key=True)
  description = db.Column(db.String, nullable=False)
  completed = db.Column(db.Boolean, default=False, nullable=True)
  list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False, default=1)

  def __repr__(self):
      return f'<Todo | id:{self.id} | description:{self.description} | completed:{self.completed}>'
  
class TodoList(db.Model):
  __tablename__ = 'todolists'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  todos = db.relationship('Todo', backref='list', lazy=True) 
  
  def __repr__(self):
      return f'<Todolist | id:{self.id} | name:{self.name} | todos_fk:{self.todos}>'

@app.route('/')
def index():
  # return render_template('index.html', data=Todo.query.order_by('id').all())
  return redirect(url_for('get_list_todos', list_id=1))

@app.route('/create', methods=['POST'])
def create():
  """Creates a todo in the default todo-list (id: 1)"""

  error = False
  body = {}
  try:
    _description = request.get_json()['description'] # returns a dictionary 
    _todo = Todo(description = _description)
    db.session.add(_todo)
    db.session.commit()
    body['description'] = _todo.description 
    body['completed'] = _todo.completed
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  return jsonify(body)

@app.route('/lists/<int:_id>/todo/create', methods=['POST'])
def create_list_todo(_id):
  error = False
  body = {}
  try:
    _description = request.get_json()['description'] # returns a dictionary 
    _list_id = request.get_json()['list_id'] # returns a dictionary 
    _todo = Todo(description = _description, list_id = _list_id )
    db.session.add(_todo)
    db.session.commit()
    body['id'] = _todo.id 
    body['description'] = _todo.description 
    body['completed'] = _todo.completed
    body['list_id'] = _todo.list_id
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  return jsonify(body)


@app.route('/<int:_id>', methods=['POST'])
def update(_id):
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


@app.route('/<int:_id>/delete', methods=['DELETE'])
def delete(_id):
  error = False
  response = {}
  try:
    print(request.get_json()) 
    _todo = Todo.query.get(_id)
    print(_todo)
    db.session.delete(_todo)
    # Todo.query.filter_by(id=_id).delete
    db.session.commit()
  except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
    response = {"success": True}
  if error:
    abort(400)
  return jsonify(response)
    


@app.route('/<int:_id>/set-completed', methods=['POST'])
def set_completed_todo(_id):
  error = False
  body = {}
  try: 
    _todo = Todo.query.get(_id)
    completed = request.get_json()['completed']
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
  return redirect(url_for('index'))

@app.route('/lists/<int:list_id>', methods=['GET'])
def get_list_todos(list_id):
  return render_template('index.html',
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(list_id),
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()
  )

@app.route('/lists/create', methods=['POST'])
def create_list():
  body = {}
  error = False
  print(request.get_json())
  try:
    _name = request.get_json()['name']
    _todolist = TodoList(name = _name)
    db.session.add(_todolist)
    db.session.commit()
    body['id'] = _todolist.id
    body['name'] = _todolist.name 
  except:
    error=True
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()
  if error:
    abort(400)
  return jsonify(body)
