
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://User:saraBarabu0@localhost/project_tracker'
app.config['SECRET_KEY'] = '\xeatj\xbcgk\x8e0W\xe6\x06\x8d\x12\x13\xef\xca\xb5\x8aa\xa7I\xcf\xf9\x18'

db = SQLAlchemy(app)

class Project(db.Model):
    __tablename__ = 'projects'

    project_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.project_id'))
    description = db.Column(db.String(100))

    project = db.relationship('Project')


@app.route('/')
def show_projects():
    return render_template('index.html', projects = Project.query.all())

@app.route('/project/<project_id>')
def show_tasks(project_id):
    return render_template('project_tasks.html',
                           project=Project.query.filter_by(project_id=project_id).first(),
                           tasks = Task.query.filter_by(project_id=project_id))

@app.route('/add/project', methods=['post'])
def add_project():

    title = request.form['projecttitle']
    if title:
        new_project = Project(title = title)
        db.session.add(new_project)
        db.session.commit()
        flash('New project added successfully', 'green')
    else:
        flash('Enter a title for your new project', 'red')
    return redirect(url_for('show_projects'))

@app.route('/add/task/<project_id>', methods=['post'])
def add_task(project_id):
    # add task
    description = request.form['taskdescription']
    if description:
        new_task = Task(project_id=project_id, description = description)
        db.session.add(new_task)
        db.session.commit()
        flash('New task added successfully', 'green')
    else:
        flash('Enter a description for your new task', 'red')
    return redirect(url_for('show_tasks', project_id=project_id))

@app.route('/delete/task/<project_id>', methods=['post'])
def del_task(project_id):
    task_id = request.form['taskid']
    if task_id:
        tasktodel = Task.query.filter_by(task_id=task_id).first()
        if tasktodel:
            db.session.delete(tasktodel)
            db.session.commit()
            flash('The task was successfully deleted', 'green')
        else:
            flash('There is no task with suth an ID', 'red')
    else:
        flash('Enter an ID of a task to delete', 'red')
    return redirect(url_for('show_tasks', project_id=project_id))

@app.route('/delete/project/', methods=['post'])
def del_project():
    project_id = request.form['projectid']
    all_tasks = request.form.get('plustasks')
    if project_id:
        projecttodel = Project.query.filter_by(project_id=project_id).first()
        if projecttodel:
            if all_tasks=='checked':
                taskstodel = Task.query.filter_by(project_id=project_id).all()
                for tasktodel in taskstodel:
                    db.session.delete(tasktodel)
                    db.session.flush()
                db.session.delete(projecttodel)
                db.session.commit()
                flash('The project and all tasks were successfully deleted', 'green')
            else:
                db.session.delete(projecttodel)
                db.session.commit()
                flash('The project was successfully deleted', 'green')
        else:
            flash('There is no project with suth an ID', 'red')
    else:
        flash('Enter an ID of a project to delete', 'red')
    return redirect(url_for('show_projects'))



app.run(debug=True, host='127.0.0.1', port=3000)