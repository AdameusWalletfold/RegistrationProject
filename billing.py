# ----------------------------------------------------------------
# Author: Mihir Vadadoria, Adam Knott
# Date: 4/25/2023
#
# This module calculates and displays billing information
# for students in the class registration system.  Student and
# class records are reviewed and tuition fees are calculated.
# -----------------------------------------------------------------

def calculate_hours_and_bill(id, s_in_state, c_rosters, c_hours):
    # ------------------------------------------------------------
    # This function calculate billing information. It takes four
    # parameters: id, the student id; s_in_state, the list of
    # in-state students; c_rosters, the rosters of students in
    # each course; c_hours, the number of hours in each course.
    # This function returns the number of course hours and tuition
    # cost.
    # ------------------------------------------------------------
    hours = 0
    cost = 0
    for course in c_rosters:
        if id in c_rosters[course]:
            hours += c_hours[course]
            if not s_in_state.get(id):
                cost += c_hours[course] * 850
            else:
                cost += c_hours[course] * 225
    return hours, cost


def display_hours_and_bill(hours, cost):
    pass
