from flask import Flask, render_template, request

import hackbright_app

app = Flask(__name__)

@app.route("/")
def get_github():
    return render_template("get_github.html")

@app.route("/student")
def get_student():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")
    rows = hackbright_app.get_all_grades_by_student(student_github)
    # print "row is %r" % row
    html = render_template("student_grades.html", github =student_github,
                                                rows = rows)
    return html

@app.route("/project")
def project_grades():
    hackbright_app.connect_to_db()
    myproject_title = request.args.get("project")
    rows = hackbright_app.get_all_grades_by_title(myproject_title)
    print "********************************************"
    print rows
    html = render_template("project_grades.html", project =myproject_title,
                                                rows = rows)
    return html

@app.route("/newstudent")
def get_new_student():
    hackbright_app.connect_to_db()
    first_name = request.args.get("firstname")
    last_name = request.args.get("lastname")
    student_github = request.args.get("github")
    hackbright_app.make_new_student(first_name, last_name, student_github)
    html = render_template("student_info.html", first_name = first_name, 
                                                last_name = last_name,
                                                github = student_github)
    return html

@app.route("/makenewstudent")
def makenewstudent():
    return render_template("make_new_student.html")

@app.route("/newproject")
def get_new_project():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    description = request.args.get("description")
    max_grade = request.args.get("max_grade")
    hackbright_app.make_new_project(project_title, description, max_grade)
    html = render_template("project_info.html", project = project_title, 
                                                description = description,
                                                max_grade = max_grade)
    return html

@app.route("/makenewproject")
def makenewproject():
    return render_template("make_new_project.html")

@app.route("/getstudentgrade")
def get_new_grade_for_student():
    return render_template("get_student_grade.html")    

@app.route("/givestudentgrade")
def give_new_grade_to_student():
    hackbright_app.connect_to_db()
    project_title = request.args.get("project")
    student_github = request.args.get("github")
    grade = request.args.get("grade")
    rows = hackbright_app.give_student_a_grade(student_github, project_title, grade)
    print "*************************"
    print rows
    html = render_template("student_grades.html", github =student_github,
                                                rows = rows)
    return html


if __name__ == "__main__":
    app.run(debug=True)