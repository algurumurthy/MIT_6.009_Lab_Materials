#!/usr/bin/env python3
"""6.009 Lab 6 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def update_unit_clauses(CNF, assignment):
    """
    Helper function to better understand where to place unit clauses. Given a 
    CNF and a temporary assignment of sorts, it will loop through and check for
    any sub cluases of len(1) returning an updated assignment as well
    as the CNF that was inputted
    """
    for sub_clause in CNF:
        if len(sub_clause) == 1:
            assignment[sub_clause[0][0]] = sub_clause[0][1]
            update = formula_update(CNF, sub_clause[0])
            if update is None:
                return (None, None)
            return update_unit_clauses(update, assignment)
    return CNF, assignment


def final_index(lista):
    """
    Given a list, returns the final index in the list at inputted length
    """
    return len(lista) -1 


def formula_update(CNF, value):
    """
    This updates any inputted CNF by a given value (tuple) that might be 
    inputted and returns the list (or in this case, updated CNF function)
    """
    new_CNF = []
    if CNF == []:
        return []
    for sub_clause in CNF:
        #if you have an empty list anywhere, then it immediately fails ot satisfy
        if sub_clause == []:
            return None
        if value not in sub_clause:
            im_list = []
            for tup in sub_clause:
                if value[0] != tup[0]:
                    im_list.append(tup)
            new_CNF.append(im_list)
    return new_CNF


def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    assignment = {}
    updated_CNF, updated_assignment = update_unit_clauses(formula, assignment)
    #base cases:
    if updated_CNF == None:
        return None
    if len(updated_CNF) == 0:
        return updated_assignment
    if [] in updated_CNF:
        return None
    for clause in formula:
        #look through all the cases where some value is being set to True
        for sub_clause in clause:
            first_formula_clause = sub_clause[0]
            updated2 = formula_update(updated_CNF, (first_formula_clause, True))
            true_path = satisfying_assignment(updated2)
            if true_path is not None:
                true_path[first_formula_clause] = True
                true_path.update(updated_assignment)
                return true_path
        #look through all the cases where some value is being set to False
            updated2 = formula_update(updated_CNF, (first_formula_clause, False))
            false_path = satisfying_assignment(updated2)
            if false_path is not None:
                false_path[first_formula_clause] = False
                false_path.update(updated_assignment)
                return false_path
        #if both looping through true and false return nothing, then we know that
        #there is no solution to the associated CNF
            return None


def val_end_position(any_list):
    """
    Given a list, returns the final value in the list 
    """
    return any_list[final_index(any_list)]

    
def help_groups(students, group_size):
    """
    Given some dictionary of students an a desired group size, creates all possible
    combinations of groups in a data via returning a set
    """
    if group_size == 1:
        student_list = []
        for element in students:
            student_list.append(frozenset([element]))
        return student_list
    else:
        grouping2 = set()
        for i in range(len(students)):
            reduced_list = students[i+1:]
            for remaining_students in help_groups(reduced_list, group_size - 1):
                grouping2.add(frozenset([students[i]]) | remaining_students)
        return grouping2


def boolify_scheduling_problem(student_preferences, session_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """
    def first_rule(student_preferences, session_capacities):
        """
        Given student preferences and session capacities, will go through first 
        and make sure that every student gets at least one of their preferences
        and returns a list with the appropriate representative rule
        """
        
        first_rule = []
        
        for ID, time_choice in student_preferences.items():
            
            first_rule.append([])
            
            for time in time_choice:
                
                val_end_position(first_rule).append((ID + '_' + time, True))
                
        return first_rule
    
    
    
    def second_rule(student_preferences, session_capacities):
        """
        This rule is split into two peices such that each student is put into 
        one session but no more than 1 session per student. So given the 
        student preferences and the session capacities, it will return the 
        rule (list) that gives us the appropriate assignment for this condition.
        """
        
        time_limits = session_capacities.keys()
        
        rule2 = []
        
        for ID, time_choice in student_preferences.items():
            #find groups of 2 because we want to make sure that we have no more
            #than one per student at all times!
            im_groups = help_groups(list(time_limits), 2)
            
            for block in im_groups:
                
                im_list = []
                
                for time in block:
                    
                    time = (ID + '_' + time, False)
                    
                    im_list.append(time)
                    
                rule2.append(im_list)
                
        return rule2
    
    
    
    def third_rule(student_preferences, session_capacities):
        """
        We need to make sure that the session is not "oversubscribed" so in order
        to do that given the student preferences and the session capacities, 
        we are goign to return a list (rule) that applies/accounts for this case
        """
        
        ID = student_preferences.keys()
        
        rule3 = []
        
        for s_id, time_limit in session_capacities.items():
            
            if time_limit < len(ID):
                #account for the fact that we need to look at N+1 instead of N
                im_groups = help_groups(list(ID), time_limit+1)
                
                for block in im_groups:
                    
                    im_list = []
                    
                    for time in block:
                        
                        time = (time + '_' + s_id, False)
                        
                        im_list.append(time)
                        
                    rule3.append(im_list)
                    
                    
        return rule3
    # add all the rules to create one cohesive rule that can satisfy all given conditions
    CNF = first_rule(student_preferences, session_capacities) + second_rule(student_preferences, session_capacities) + third_rule(student_preferences, session_capacities)
    return CNF


if __name__ == '__main__':
#    import doctest
#    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
#    doctest.testmod(optionflags=_doctest_flags)
#    s = boolify_scheduling_problem({'Alice': {'basement', 'penthouse'},
#                            'Bob': {'kitchen'},
#                            'Charles': {'basement', 'kitchen'},
#                            'Dana': {'kitchen', 'penthouse', 'basement'}},
#                           {'basement': 1,
#                            'kitchen': 2,
#                            'penthouse': 4})
#    print(s)
    students = [1, 2, 3, 4]
    print(help_groups(students, 2))
