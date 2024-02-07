from flask import Flask, jsonify, request, redirect
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

# Import for Migrations
from flask_migrate import Migrate, migrate
 

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Settings for migrations
migrate = Migrate(app, db)

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
    return render_template('index.html')

@app.route('/add_data')
def add_data():
    return render_template('add_profile.html')

@app.route('/tasks')
def get_tasks():
    tasks = Todo.query.all()
    output = []
    for task in tasks:
        task_data = {'title': task.title, 'description': task.description, 'completed': task.completed}
        output.append(task_data)
    return {"tasks": output}










# function to add profiles
@app.route('/add', methods=["POST"])
def profile():
	
	# In this function we will input data from the 
	# form page and store it in our database.
	# Remember that inside the get the name should
	# exactly be the same as that in the html
	# input fields
	first_name = request.form.get("first_name")
	last_name = request.form.get("last_name")
	age = request.form.get("age")

	# create an object of the Profile class of models
	# and store data as a row in our datatable
	if first_name != '' and last_name != '' and age is not None:
		p = Profile(first_name=first_name, last_name=last_name, age=age)
		db.session.add(p)
		db.session.commit()
		return redirect('/')
	else:
		return redirect('/')








@app.route('/tasks', methods=['POST'])
def add_task():
    task = Todo(title=request.json['title'], description=request.json['description'], completed=request.json['completed'])
    db.session.add(task)
    db.session.commit()
    return {'id': task.id}






















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



@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Todo.query.get(id)
    if task is None:
        return {"error": 404}
    db.session.delete(task)
    db.session.commit()
    return {'message': f'Task with id: ${id} has been deleted'}


if __name__ == '__main__':
    app.run()