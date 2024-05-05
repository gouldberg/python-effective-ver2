#!/usr/bin/env PYTHONHASHSEED=1234 python3

from collections import defaultdict
from collections import namedtuple


# ------------------------------------------------------------------------------
# SimpleGradeBook: dictionary is used
# ------------------------------------------------------------------------------

class SimpleGradebook:
    def __init__(self):
        # dictionary
        self._grades = {}

    def add_student(self, name):
        # element is list
        self._grades[name] = []

    def report_grade(self, name, score):
        self._grades[name].append(score)

    def average_grade(self, name):
        grades = self._grades[name]
        return sum(grades) / len(grades)


book = SimpleGradebook()

book.add_student('Isaac Newton')
book.report_grade('Isaac Newton', 90)
book.report_grade('Isaac Newton', 95)
book.report_grade('Isaac Newton', 85)

print(book._grades)
print(book.average_grade('Isaac Newton'))


# ------------------------------------------------------------------------------
# Use defaultdict in inner dict
# ------------------------------------------------------------------------------

class BySubjectGradebook:
    def __init__(self):
        self._grades = {}                       # Outer dict

    def add_student(self, name):
        self._grades[name] = defaultdict(list)  # Inner dict

    def report_grade(self, name, subject, grade):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        grade_list.append(grade)

    def average_grade(self, name):
        by_subject = self._grades[name]
        total, count = 0, 0
        for grades in by_subject.values():
            total += sum(grades)
            count += len(grades)
        return total / count

book = BySubjectGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75)
book.report_grade('Albert Einstein', 'Math', 65)
book.report_grade('Albert Einstein', 'Gym', 90)
book.report_grade('Albert Einstein', 'Gym', 95)
print(book.average_grade('Albert Einstein'))


# ------------------------------------------------------------------------------
# requirement is more complex ....
# ------------------------------------------------------------------------------

class WeightedGradebook:
    def __init__(self):
        self._grades = {}

    def add_student(self, name):
        self._grades[name] = defaultdict(list)

    def report_grade(self, name, subject, score, weight):
        by_subject = self._grades[name]
        grade_list = by_subject[subject]
        # ----------
        # here tuple (score, weight)
        grade_list.append((score, weight))

    def average_grade(self, name):
        by_subject = self._grades[name]

        score_sum, score_count = 0, 0
        for subject, scores in by_subject.items():
            subject_avg, total_weight = 0, 0
            for score, weight in scores:
                subject_avg += score * weight
                total_weight += weight

            score_sum += subject_avg / total_weight
            score_count += 1

        return score_sum / score_count


book = WeightedGradebook()
book.add_student('Albert Einstein')
book.report_grade('Albert Einstein', 'Math', 75, 0.05)
book.report_grade('Albert Einstein', 'Math', 65, 0.15)
book.report_grade('Albert Einstein', 'Math', 70, 0.80)
book.report_grade('Albert Einstein', 'Gym', 100, 0.40)
book.report_grade('Albert Einstein', 'Gym', 85, 0.60)

print(book.average_grade('Albert Einstein'))


# --> this code is not readable .... Refactoring is required.


# ------------------------------------------------------------------------------
# Refactoring to multiple classes: Subject, Student, Gradebook
#   - Subject use Grade
#   - Student use Subject
#   - Gradebook use Student
# use namedtuple 
# ------------------------------------------------------------------------------

# Use namedtuple
#   - NOTE: namedtuple does not have default value --> dataclasses is better.
#   - NOTE: attribute value of instance of namedtuple can be accessed by index and iteration --> this would be some risk in application
Grade = namedtuple('Grade', ('score', 'weight'))

class Subject:
    def __init__(self):
        self._grades = []

    def report_grade(self, score, weight):
        # ----------
        # Here namedtuple Grade is used
        self._grades.append(Grade(score, weight))
        # ----------

    def average_grade(self):
        total, total_weight = 0, 0
        for grade in self._grades:
            total += grade.score * grade.weight
            total_weight += grade.weight
        return total / total_weight


class Student:
    def __init__(self):
        # ----------
        # Here Subject class is used.
        self._subjects = defaultdict(Subject)

    def get_subject(self, name):
        return self._subjects[name]

    def average_grade(self):
        total, count = 0, 0
        for subject in self._subjects.values():
            total += subject.average_grade()
            count += 1
        return total / count


class Gradebook:
    def __init__(self):
        # ----------
        # Here Student class is used.
        self._students = defaultdict(Student)

    def get_student(self, name):
        return self._students[name]


# ----------

book = Gradebook()

albert = book.get_student('Albert Einstein')

math = albert.get_subject('Math')
math.report_grade(75, 0.05)
math.report_grade(65, 0.15)
math.report_grade(70, 0.80)

gym = albert.get_subject('Gym')
gym.report_grade(100, 0.40)
gym.report_grade(85, 0.60)

print(albert.average_grade())
