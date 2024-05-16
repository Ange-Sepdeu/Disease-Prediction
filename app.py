import sqlite3 # For sqlite database connection

from flask import Flask # used to create the app

# used to render HTML files to the browser
from flask import render_template

# used to access request information like form data, cookies, etc.
from flask import request

from create_db import get_path_to_sqlite_database

app = Flask(__name__) # create a Flask app

# gets the absolute path to this app's database, 
# the db.sqlite file created after running the create_db.py 
# script
path_to_db = get_path_to_sqlite_database(file_path=__file__)

@app.route('/', methods=["GET", "POST"])
def index():
    #TODO
    # add functionality to add a new project and student
    # to the database 
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        form = request.form
        student_name = form['name']
        project_name = form['project-name']
        project_description = form['project-description']
        with sqlite3.connect(path_to_db) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Students (name) VALUES(?)"
            cursor.execute(query, (student_name,))
            connection.commit()
            result = cursor.execute("SELECT id FROM Students ORDER BY id DESC LIMIT 1").fetchone()
            insert_project_query = "INSERT INTO Projects (student, name, description) VALUES(?,?,?)"
            cursor.execute(insert_project_query, (result[0], project_name, project_description))
            connection.commit()
            return form

@app.route('/projects', methods=["GET"])
def projects():
    #TODO
    # get list of projects from the database
    # return a dictionary of those projects to the browser
    # replace simple json output with an HTML page, containing 
    # a table of the projects
    # add styles and JavaScript to this page 
    with sqlite3.connect(path_to_db) as connection:
        cursor = connection.cursor()
        result = cursor.execute("SELECT p.name, p.description, s.name as student_name FROM Projects p LEFT JOIN Students s On p.student=s.id").fetchall()
        connection.commit()
        results = [
            {
                "project": {
                    "name": f[0],
                    "description": f[1]
                },
                "student": {
                    "name": f[2]
                }
            } for f in result
        ] 
        return results