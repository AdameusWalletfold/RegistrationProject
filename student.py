# ----------------------------------------------------------------
# Author: Mihir Vadadoria, Adam Knott
# Date: 4/25/2023
#
# This module supports changes in the registered courses
# for students in the class registration system.  It allows
# students to add courses, drop courses and list courses they are
# registered for.
# -----------------------------------------------------------------


def list_courses(id, c_roster):
    # ------------------------------------------------------------
    # This function displays and counts courses a student has
    # registered for.  It has two parameters: id is the ID of the
    # student; c_roster is the list of class rosters. This function
    # has no return value.
    # -------------------------------------------------------------
    course_count = 0
    course_list = []
    for course in c_roster:
        if id in c_roster[course]:
            course_count += 1
            course_list.append(course)
    return course_list, course_count


def add_course(id, course, c_roster, c_max_size):
    # ------------------------------------------------------------
    # This function adds a student to a course.  It has three
    # parameters: id is the ID of the student to be added; c_roster is the
    # list of class rosters; c_max_size is the list of maximum class sizes.
    # This function asks user to enter the course he/she wants to add.
    # If the course is not offered, display error message and stop.
    # If student has already registered for this course, display
    # error message and stop.
    # If the course is full, display error message and stop.
    # If everything is okay, add student ID to the course’s
    # roster and display a message if there is no problem.  This
    # function has no return value.
    # -------------------------------------------------------------
    try:
        if course not in c_roster:
            return "Course not found"
        elif id in c_roster[course]:
            return "You are already enrolled in that course."
        elif len(c_roster[course]) >= c_max_size[course]:
            return "Course already full."
        else:
            c_roster[course].append(id)
            return "Course added"
    except KeyError:
        return


def drop_course(course, id, c_roster):
    # ------------------------------------------------------------
    # This function drops a student from a course.  It has two
    # parameters: id is the ID of the student to be dropped;
    # c_roster is the list of class rosters. This function asks
    # the user to enter the course he/she wants to drop.  If the course
    # is not offered, display error message and stop.  If the student
    # is not enrolled in that course, display error message and stop.
    # Remove student ID from the course’s roster and display a message
    # if there is no problem.  This function has no return value.
    # -------------------------------------------------------------
    try:
        if course not in c_roster:
            return "Course not found"
        if id not in c_roster[course]:
            return "You are not enrolled in that course."
        c_roster[course].remove(id)
        return "Course dropped"
    except KeyError:
        pass
