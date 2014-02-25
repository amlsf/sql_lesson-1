import sqlite3

DB = None
CONN = None

def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    # No need to return anything, right? 

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    return row 

def get_project_by_title(title):
    query="""SELECT title, description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
    Project: %s
    Description: %s
    Max grade: %d"""%(row[0], row[1], row[2])

def make_new_project(title, description, max_grade):
    query = """INSERT into Projects values (NULL, ?, ?, ?)"""
    DB.execute(query, (title, description, int(max_grade)))
    CONN.commit()
    print "Successfully added project: %s %s %d"%(title, description, int(max_grade))
# TODO add checks for whether project already exists. Is it case sensitive? 

def get_grade_by_project(student_github, project_title):
    query = """SELECT student_github, project_title, grade FROM Grades WHERE student_github = ? AND project_title = ?"""
    DB.execute(query, (student_github, project_title))
    row = DB.fetchone()
    print """\
    Student github : %s
    Project title : %s
    Grade: %d"""%(row[0], row[1], row[2])

def give_grade(student_github, project_title, grade):
    query = """INSERT into Grades values (?, ?, ?)"""
    DB.execute(query, (student_github, project_title, grade))
    CONN.commit()
    # print "Successfully added grade: %s %s %d"%(student_github, project_title, grade)

def get_grades_by_student(student_github):
    query = """SELECT grade, project_title FROM Grades WHERE student_github = ?"""
    DB.execute(query, (student_github,))
    row = DB.fetchone()
    list_of_grades = []
    while row != None:
        list_of_grades.append({'grade':row[0],'project_title':row[1]})
        row = DB.fetchone()
    return list_of_grades

# Create new function to get all student githubs for webapp
def get_all_studentgrades(project_title):
    query = """SELECT student_github, grade FROM Grades WHERE project_title = ?"""
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    list_of_studentgrades = []
    while row != None:
        list_of_studentgrades.append({'github':row[0],'grade':row[1]})
        row = DB.fetchone()
    return list_of_studentgrades


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project":
            get_project_by_title(*args)
        elif command == "new_project":
            make_new_project(*args)
        elif command == "grade":
            get_grade_by_project(*args)
        elif command == "assign_grade":
# TODO Need to add checks if project exists. How would you display on webpage? (create a new page?)
            give_grade(*args)
        elif command == "show_grades":
            get_grades_by_student(*args)
        elif command == "project_grades":
            get_all_studentgrades(*args)

    CONN.close()

if __name__ == "__main__":
    main()
