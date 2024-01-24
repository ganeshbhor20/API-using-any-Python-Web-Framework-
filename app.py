from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Project model
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

# UserProject model
class UserProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)

# TaskProject model
class TaskProject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userproject_id = db.Column(db.Integer, db.ForeignKey('user_project.id'), nullable=False)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)

# API endpoint to add UserProject entry
@app.route('/add_user_project', methods=['POST'])
def add_user_project():
    data = request.get_json()
    user_id = data.get('user_id')
    project_name = data.get('project_name')

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    project = Project.query.filter_by(name=project_name).first()
    if not project:
        project = Project(name=project_name)
        db.session.add(project)
        db.session.commit()

    user_project = UserProject(user_id=user_id, project_id=project.id)
    db.session.add(user_project)
    db.session.commit()

    return jsonify({'message': 'UserProject entry added successfully'}), 201

# API endpoint to add TaskProject entry
@app.route('/add_task_project', methods=['POST'])
def add_task_project():
    data = request.get_json()
    user_project_id = data.get('user_project_id')
    task_id = data.get('task_id')

    # Use db.session.get() instead of Query.get()
    user_project = db.session.get(UserProject, user_project_id)
    print("user_project:", user_project)  # Debug line

    if not user_project:
        return jsonify({'error': 'UserProject entry not found'}), 404

    task = Task.query.get(task_id)
    print("task:", task)  # Debug line

    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Sample tasks should be added before creating TaskProject entry
    sample_task1 = Task(name="Task1")
    sample_task2 = Task(name="Task2")

    db.session.add_all([sample_task1, sample_task2])
    db.session.commit()

    task_project = TaskProject(userproject_id=user_project_id, task_id=task_id)
    db.session.add(task_project)
    db.session.commit()

    return jsonify({'message': 'TaskProject entry added successfully'}), 201



# API endpoint to get TaskProject entry
@app.route('/get_task_project/<int:user_id>', methods=['GET'])
def get_task_project(user_id):
    user_projects = UserProject.query.filter_by(user_id=user_id).all()

    result = []
    for user_project in user_projects:
        user_name = User.query.get(user_project.user_id).name
        project_name = Project.query.get(user_project.project_id).name

        task_projects = TaskProject.query.filter_by(userproject_id=user_project.id).all()
        for task_project in task_projects:
            task_name = Task.query.get(task_project.task_id).name

            entry = {
                'User_id': user_project.user_id,
                'User_name': user_name,
                'Project_id': user_project.project_id,
                'Project_name': project_name,
                'Task_id': task_project.task_id,
                'Task_name': task_name
            }
            result.append(entry)

    return jsonify(result)
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()

        # Add sample users to the database
        sample_user1 = User(name="John Doe")
        sample_user2 = User(name="Jane Doe")

        db.session.add_all([sample_user1, sample_user2])
        db.session.commit()

        # Add sample projects to the database
        sample_project1 = Project(name="Project ABC")
        sample_project2 = Project(name="Project XYZ")

        db.session.add_all([sample_project1, sample_project2])
        db.session.commit()

        # Add sample tasks to the database
        sample_task1 = Task(name="Task 1")
        sample_task2 = Task(name="Task 2")

        db.session.add_all([sample_task1, sample_task2])
        db.session.commit()

    app.run(debug=True)
