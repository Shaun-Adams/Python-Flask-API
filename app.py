from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed
        }

@app.route('/')
def index():
    return 'Hello!'

@app.route('/tasks')
def get_tasks():
    tasks = Todo.query.all()
    output = []
    for task in tasks:
        task_data = {'title': task.title, 'description': task.description, 'completed': task.completed}
        output.append(task_data)
    return {"tasks": output}


@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    if 'title' in request.json:
        task.title = request.json['title']
    if 'description' in request.json:
        task.description = request.json['description']
    if 'completed' in request.json:
        task.completed = request.json['completed']
    db.session.commit()
    return jsonify(task.__repr__())

@app.route('/tasks/<id>')
def get_task(id):
    task = Todo.query.get_or_404(id)
    return jsonify({'title': task.title, 'description': task.description, 'completed': task.completed})

@app.route('/tasks', methods=['POST'])
def add_task():
    task = Todo(title=request.json['title'], description=request.json['description'], completed=request.json['completed'])
    db.session.add(task)
    db.session.commit()
    return {'id': task.id}


@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Todo.query.get(id)
    if task is None:
        return {"error": 404}
    db.session.delete(task)
    db.session.commit()
    return {'message': f'Task with id: ${id} has been deleted'}
