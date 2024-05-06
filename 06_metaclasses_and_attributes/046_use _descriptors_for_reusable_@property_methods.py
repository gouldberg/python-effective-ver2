#!/usr/bin/env PYTHONHASHSEED=1234 python3

from weakref import WeakKeyDictionary


# ------------------------------------------------------------------------------
# class Homework, Exam
# getter(@property) and setter(@grade.setter)
# repeating getter and setter to writing_grade, math_grade ....
# ------------------------------------------------------------------------------

class Homework:
    def __init__(self):
        self._grade = 0

    @property
    def grade(self):
        return self._grade

    @grade.setter
    def grade(self, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._grade = value

# repeating getter and setter to writing_grade, math_grade ....
class Exam:
    def __init__(self):
        self._writing_grade = 0
        self._math_grade = 0

    @staticmethod
    def _check_grade(value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')

    @property
    def writing_grade(self):
        return self._writing_grade

    @writing_grade.setter
    def writing_grade(self, value):
        self._check_grade(value)
        self._writing_grade = value

    @property
    def math_grade(self):
        return self._math_grade

    @math_grade.setter
    def math_grade(self, value):
        self._check_grade(value)
        self._math_grade = value


galileo = Homework()
galileo.grade = 95
assert galileo.grade == 95

galileo = Exam()
galileo.writing_grade = 85
galileo.math_grade = 99

assert galileo.writing_grade == 85
assert galileo.math_grade == 99


# ------------------------------------------------------------------------------
# Descriptor class, implemented with __get__ and __set__
# ------------------------------------------------------------------------------

class Grade:
    def __get__(self, instance, instance_type):
        pass

    def __set__(self, instance, value):
        pass


class Exam:
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


exam = Exam()


# ----------
# set
exam.writing_grade = 40
# above is same as:
Exam.__dict__['writing_grade'].__set__(exam, 40)


# ----------
# get
exam.writing_grade

# above is same as:
# 
Exam.__dict__['writing_grade'].__get__(exam, Exam)


# ------------------------------------------------------------------------------
# Descriptor class (Grade) updated
# but Grade instance is created only once ... (shared among all instances)
# ------------------------------------------------------------------------------

class Grade:
    def __init__(self):
        self._value = 0

    def __get__(self, instance, instance_type):
        return self._value

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._value = value

# Grade instance is created only once at Exam instance is created !!
class Exam:
    # Class attributes
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


# ----------
# 1st exam
first_exam = Exam()

# set
first_exam.writing_grade = 82
first_exam.science_grade = 99

# OK
print('Writing', first_exam.writing_grade)
print('Science', first_exam.science_grade)


# ----------
# 2nd exam

# now create other instance ...
second_exam = Exam()

# and set
second_exam.writing_grade = 75

print(f'Second {second_exam.writing_grade} is right')

# first_exam result is modified .... (82 --> 75)
print(f'First  {first_exam.writing_grade} is wrong; '
      f'should be 82')


# ------------------------------------------------------------------------------
# Descriptor class (Grade) updated
# save state for each instance at setter
# ------------------------------------------------------------------------------

class Grade:
    def __init__(self):
        self._values = {}

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        # ----------
        # now save for each instance.
        # but problem is memory leak ... reference counter for this instance never be zero and not garbage collected.
        # ----------
        self._values[instance] = value


# ------------------------------------------------------------------------------
# Descriptor class (Grade) updated
# WeakKeyDictionary():
# If Exam instance is not referenced, dictionary _values is empty.
# This will avoid memory leak.
# ------------------------------------------------------------------------------

class Grade:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, instance_type):
        if instance is None:
            return self
        return self._values.get(instance, 0)

    def __set__(self, instance, value):
        if not (0 <= value <= 100):
            raise ValueError(
                'Grade must be between 0 and 100')
        self._values[instance] = value


class Exam:
    math_grade = Grade()
    writing_grade = Grade()
    science_grade = Grade()


first_exam = Exam()
first_exam.writing_grade = 82

second_exam = Exam()
second_exam.writing_grade = 75

print(f'First  {first_exam.writing_grade} is right')

# now correctly get 75 not 82.
# (by WeakKeyDictionary, first_exam instance is deleted at second instance is created)
print(f'Second {second_exam.writing_grade} is right')
