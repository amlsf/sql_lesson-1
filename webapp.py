from flask import Flask, render_template, request
import hackbright_app

app = Flask(__name__)

# web app to get github to get student grades
@app.route("/")
def get_github():
    return render_template("get_github.html")

# student grades for all projects, allows to click on projects to get all student grades
@app.route("/studentgrades")
def get_studentgrades():
    hackbright_app.connect_to_db()
    student_github = request.args.get("student")
    rows = hackbright_app.get_grades_by_student(student_github)
    html = render_template("student_info.html", rows = rows , student_github = student_github)
# Note need to put student_github in there so it passes through Jinja - left side goes to Jinja/html, right side references python var
    return html

# get all student grades for particular project with links back to particular grades on all projects
@app.route("/allgrades/<projectname>")
def get_projectgrades(projectname):
    hackbright_app.connect_to_db()
    # project_title = request.args.get("projectname") #Don't need this because active user input not in URL or web form
    projects = hackbright_app.get_all_studentgrades(projectname)
    html = render_template("project_grades.html", projects = projects)
    return html
# When take to route/URL, telling to render function. So URL:function key:value pair
#   When enter URL, like going to command line and calling python file to activate function

# pair of handlers that allows user to create a new student record
@app.route("/addstudent")
def get_addstudent():
    return render_template("get_addstudent.html")

@app.route("/newstudent")
def addstudent():
    hackbright_app.connect_to_db()
    student_firstname = request.args.get("firstname")
    student_lastname = request.args.get("lastname")
    student_github = request.args.get("github")
    hackbright_app.make_new_student(student_firstname, student_lastname, student_github)
    html = render_template("addednewstudent.html", student_firstname = student_firstname, 
            student_lastname = student_lastname, student_github = student_github)
    return html

# pair of handlers that user to create a new project record
@app.route("/addproject")
def get_addproject():
    return render_template("get_addproject.html")

@app.route("/newproject")
def addproject():
    hackbright_app.connect_to_db()
    projecttitle = request.args.get("title")
    projectdescription = request.args.get("description")
    maxprojectgrade = request.args.get("maxgrade")
    hackbright_app.make_new_student(projecttitle, projectdescription, maxprojectgrade)
    html = render_template("addednewproject.html", projecttitle = projecttitle, 
            projectdescription = projectdescription, maxprojectgrade = maxprojectgrade)
    return html

# pair of handlers to add grade on given project
@app.route("/addgrade")
def get_addgrade():
    return render_template("get_addgrade.html")


# TODO (Optional) How would you display student name with github? 
@app.route("/newgrade")
def addgrade():
    hackbright_app.connect_to_db()
    student_github = request.args.get("github")
    project_title = request.args.get("project")
    student_grade = request.args.get("grade")
    hackbright_app.give_grade(student_github, project_title, student_grade)
    html = render_template("addedgrade.html", project_title = project_title, 
            student_github = student_github, student_grade = student_github)
    return html


if __name__ == "__main__":
    app.run(debug=True)