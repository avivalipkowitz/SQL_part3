import sqlite3

DB = None
CONN = None

def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])
    return row  



def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values (?, ?, ?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name, last_name)

def get_project_description(project_title):
    query = """SELECT title, description FROM Projects WHERE title=(?) """
    DB.execute(query, (project_title,))
    row = DB.fetchone()
    print """\
Project: %s 
Project Description: %s""" % (row[0], row[1])
    return row

def give_student_a_grade(github, project_title, grade):
    query = """INSERT INTO Grades (student_github, project_title, grade) VALUES (?, ?, ?);"""
    DB.execute(query, (github, project_title, grade))
    CONN.commit()
    print "Successfully added the grade: %r to %s" %(grade, project_title)
    query = """ SELECT project_title, grade FROM Grades WHERE student_github=(?)"""
    DB.execute(query, (github,))
    rows = DB.fetchall()
    return rows

def get_all_grades_by_title(project_title):
    query = """ SELECT student_github, grade FROM Grades WHERE project_title=(?)"""
    DB.execute(query, (project_title,))
    row = DB.fetchall()
    # print """\
    # Student Github: %s
    # Project title: %s
    # Grade: %d """ % (row[0], row[1], row[2])
    return row



def make_new_project(title, description, max_grade):
    query = """INSERT INTO Projects (title, description, max_grade) VALUES (?, ?, ?)"""
    DB.execute(query, (title, description, max_grade))
    CONN.commit()
    print "Successfully added Project: %s" %title

def get_grade_by_title(github, project_title):
    query = """ SELECT student_github, project_title, grade FROM Grades WHERE student_github=(?) AND project_title=(?)"""
    DB.execute(query, (github, project_title))
    row = DB.fetchone()
    print """\
    Student Github: %s
    Project title: %s
    Grade: %d """ % (row[0], row[1], row[2])
    return row

def get_all_grades_by_student(github):
    query = """SELECT project_title, grade FROM Grades WHERE student_github = (?)"""
    DB.execute(query, (github, ))
    row = DB.fetchall()
    print """ All grades for %s: """ % github
    # for index in range(0, len(row)):
    #     # for item in row[index]:
    #     print """ %r """ % row[index]
    print row
    return row

def main():
    connect_to_db()
    command = None
    argument_list = []

    while command != "quit":
        input_string = raw_input("HBA Database> ")
        temp_arg_list = input_string.split()
        if temp_arg_list[0]=="new_project":
            new_input_string = input_string.split("\"")
            first_two_args = new_input_string[0].split()

            first_two_args.append(new_input_string[1])
            first_two_args.append(new_input_string[2])
    
            argument_list = first_two_args
            command = argument_list[0]
            args = argument_list[1:]

        else:
            tokens = input_string.split()
            command = tokens[0]
            args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "projects":
            get_project_description(*args) 
        elif command == "new_project":
            make_new_project(*args)  
        elif command == "grade":
            get_grade_by_title(*args)
        elif command == "new_grade":
            give_student_a_grade(*args) 
        elif command == "all_grades":
            get_all_grades_by_student(*args)
        elif command == "grades_by_project" :
            get_all_grades_by_title(*args)    

    CONN.close()

if __name__ == "__main__":
    main()
