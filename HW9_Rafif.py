#Author: Rafif

import unittest
import os
from prettytable import PrettyTable
from collections import defaultdict
   
class Student:  
    def __init__(self, CWID, name, major):
        """store student details"""
        self.CWID = CWID
        self.name = name
        self.major = major
        
        """ used defaultdict to store taken courses of each student associated with their grades, 
            where course is the key and grade is the value
        """
        self.taken_courses = defaultdict(str)
        
    def std_course(self, course, grade):
        #Store course and grade for each student
        self.taken_courses[course] = grade
        return self.taken_courses
        
    def completed_courses(self):
        #return completed courses for each student
        valid_grade = ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        return [course for course, grade in self.taken_courses.items() if grade in valid_grade]
                
class Instructor:
    def __init__(self, CWID, name, department):
        """store instructor details"""
        self.CWID = CWID
        self.name = name
        self.department = department
        
        """ used defaultdict to store taught courses of each instructor associated with 
            num of students in each course, where course is the key and #stds is the value
        """
        self.taught_courses = defaultdict(int)  
    
    def inst_course(self, course):
        #Store course and number of students taught by each instructor
        self.taught_courses[course] += 1
        return self.taught_courses
        
class Major:
    def __init__(self, major, flag, course):
        """store major details"""
        self.major = major
        self.flag = flag
        self.course = course

        """ used dictionary to store the flag (required or electives)
            as a key and course as a value
        """
        self.courses = defaultdict(set)
        self.add_course(flag, course)
        
        """ used dictionary to store the remaining required as 'R' and electives as 'E'
            as a keys and course as a value
        """
        self.remaining = defaultdict(set)
        
    def add_course(self, flag, course):
        #Add courses in dictionary
        self.courses[flag].add(course)
        return self.courses
    
    def remaining_courses(self, completed_courses):
        #return remaining required and electives courses for each student based on major 
        remaining_required = self.courses['R'] - set(completed_courses)
        remaining_electives = ['' if set(completed_courses).intersection(self.courses['E']) else self.courses['E']]
        self.remaining['R'] = remaining_required
        self.remaining['E'] = remaining_electives
        return self.remaining
                        
class Repository:
    def __init__(self):
        self.std_db = dict() 
        self.inst_db = dict()
        self.major_db = dict()
        self.path = '/Users/rafifarab/Desktop/Stevens/Fall 2017/SSW 810'
        
        #Read Students file
        student_file = os.path.join(self.path, 'students.txt')
        reader = FileReader(student_file, 3)
        for cwid, name, major in reader.next():
            self.std_db[cwid] = Student(cwid, name, major)
        
        #Read Instructors file
        instructor_file = os.path.join(self.path, 'instructors.txt')
        reader = FileReader(instructor_file, 3)
        for cwid, name, dept in reader.next():
            self.inst_db[cwid] = Instructor(cwid, name, dept)

        #Read Grades file
        grade_file = os.path.join(self.path, 'grades.txt')
        reader = FileReader(grade_file, 4)
        for s_cwid, course, grade, i_cwid in reader.next():
            if s_cwid in self.std_db:
                self.std_db[s_cwid].std_course(course, grade)
            else:
                print('Grade for unknown student', s_cwid)
                
            if i_cwid in self.inst_db:
                self.inst_db[i_cwid].inst_course(course)
            else:
                print('Course for unknown instructor', i_cwid)
        
        #Read Majors file
        major_file = os.path.join(self.path, 'majors.txt')
        reader = FileReader(major_file, 3)
        for major, flag, course in reader.next():
            if major in self.major_db:
                self.major_db[major].add_course(flag, course)
            else:
                self.major_db[major] = Major(major, flag, course)
   
    def major_table(self):
       #Print major table
        self.major_table = PrettyTable(['Dept', 'Required', 'Electives'])
        for major in self.major_db.values():
            self.major_table.add_row([major.major, sorted(major.courses['R']), sorted(major.courses['E'])])
        print(self.major_table)

    def student_table(self):
        #Print student table
        self.std_table = PrettyTable(['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for student in self.std_db.values(): 
            self.major_db[student.major].remaining_courses(student.completed_courses())
            self.std_table.add_row([student.CWID, student.name, student.major,sorted(student.completed_courses()), 
                                    sorted(self.major_db[student.major].remaining['R']), sorted(self.major_db[student.major].remaining['E'])])
        print(self.std_table)
 
    def instructor_table(self):
        #Print instructor table
        self.inst_table = PrettyTable(['CWID', 'Name','Dept', 'Course', 'Student'])
        for instructor in self.inst_db.values():
            for course in instructor.taught_courses.keys():
                self.inst_table.add_row([instructor.CWID, instructor.name, instructor.department, course, 
                                        instructor.taught_courses[course]])
        print(self.inst_table)
                           
class FileReader():
    #Responsible for reading file
    def __init__(self, fname, num_of_fields, sep='\t'):
      self.fname = fname
      self.num_of_fields = num_of_fields
      self.sep = sep
      
      try:
        self.f = open(self.fname, 'r')
      except:
        raise FileNotFoundError(self.fname, 'cannot be opened')
        
    def next(self):
        #return each line in a file at a time (whenever called)
        with self.f:
            for row in self.f:
                line = row.strip().split(self.sep)
                if len(line) == self.num_of_fields:
                    yield line 
                else:
                    raise Exception(self.fname + ' should have ' + str(len(line)) + ' values') 
                    #raise an error when expected doesn't match the actual values
                                                                                                   
def main():
    r = Repository()
    
    print('\nStudent Summary')
    r.student_table()
    
    print('\nInstructor Summary')
    r.instructor_table()
    
    print('\nMajor Summary')
    r.major_table()
        
class StudentTest(unittest.TestCase):
    student = Student('104111', 'Rafif, A', 'SSW')
    def test_init(self):
        self.assertEqual(StudentTest.student.CWID, '104111')
        self.assertEqual(StudentTest.student.name, 'Rafif, A')
        self.assertEqual(StudentTest.student.major, 'SSW')
        
    def test_std_course(self):
        self.assertEqual(StudentTest.student.std_course('SSW810', 'A'), {'SSW810': 'A'})
        self.assertEqual(StudentTest.student.std_course('SSW555', 'A'), {'SSW810': 'A', 'SSW555': 'A'})
               
class InstructorTest(unittest.TestCase):
    instructor = Instructor('98111', 'Maha, A', 'SSW')
    def test_init(self):
        self.assertEqual(InstructorTest.instructor.CWID, '98111')
        self.assertEqual(InstructorTest.instructor.name, 'Maha, A')
        self.assertEqual(InstructorTest.instructor.department, 'SSW')
        
    def test_inst_course(self): 
        self.assertEqual(InstructorTest.instructor.inst_course('SSW810'), {'SSW810': 1})
        self.assertEqual(InstructorTest.instructor.inst_course('SSW555'), {'SSW810': 1, 'SSW555': 1})
        self.assertEqual(InstructorTest.instructor.inst_course('SSW555'), {'SSW810': 1, 'SSW555': 2})
                                                                    
class FileReaderTest(unittest.TestCase):
    f = FileReader('/Users/rafifarab/Desktop/Stevens/Fall 2017/SSW 810/students.txt', 3)
    def test_init(self):
        self.assertRaises(FileNotFoundError, FileReader.__init__, FileReaderTest.f, 
                            '/Users/rafifarab/Desktop/Stevens/Fall 2017/SSW 810/w.txt', 3)
                            
class MajorTest(unittest.TestCase):
    student = Major('SSW', 'R', 'SSW810')
    def test_init(self):
        self.assertEqual(MajorTest.student.major, 'SSW')
        self.assertEqual(MajorTest.student.flag, 'R')
        self.assertEqual(MajorTest.student.course, 'SSW810')
        
    def test_add_course(self):
        self.assertEqual(MajorTest.student.add_course('R', 'SSW810'), {'R': {'SSW810'}})
        self.assertEqual(MajorTest.student.add_course('R', 'SSW555'), {'R': {'SSW555', 'SSW810'}})
        self.assertEqual(MajorTest.student.add_course('E', 'CS501'), {'R': {'SSW555', 'SSW810'}, 'E': {'CS501'}})

    def test_remaining_courses(self):
        completed_course = {'SSW810', 'SSW555', 'CS501'} 
        self.assertEqual(MajorTest.student.remaining_courses(completed_course), {'R': set(), 'E': ['']})  
        
if __name__ == '__main__':
        main(), unittest.main(exit = False, verbosity = 2)                                             
