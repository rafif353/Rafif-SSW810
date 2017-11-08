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
        
    def get_values(self):
        d = dict()
        d['Name'] = self.name
        d['Major'] = self.major
        d['Taken Courses'] = self.taken_courses
        return d
            
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
        
    def get_values(self):
        d = dict()
        d['Name'] = self.name
        d['Department'] = self.department
        d['Taught Courses'] = self.taught_courses
        return d  
    
    def inst_course(self, course):
        #Store course and number of students taught by each instructor
        self.taught_courses[course] += 1
        return self.taught_courses
        
class Repository:
    def __init__(self):
        self.std_db = dict() 
        self.inst_db = dict()
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
            
    def student_table(self):
        #Print student table
        self.std_table = PrettyTable(['CWID', 'Name', 'Course'])
        for cwid, val in sorted(self.std_db.items()):
            get_val = val.get_values()
            key = sorted(list(get_val['Taken Courses'].keys()))
            self.std_table.add_row([cwid, get_val['Name'], key])
        print(self.std_table)
 
    def instructor_table(self):
        #Print instructor table
        self.inst_table = PrettyTable(['CWID', 'Name','Dept', 'Course', 'Student'])
        for cwid, val in sorted(self.inst_db.items()):
            get_val = val.get_values()
            for course, num_std in get_val['Taught Courses'].items():
                self.inst_table.add_row([cwid, get_val['Name'], get_val['Department'], course, num_std])
        print(self.inst_table)
                           
class FileReader():
    def __init__(self, fname, num_of_args, sep='\t'):
      self.fname = fname
      self.num_of_args = num_of_args
      self.sep = sep
      
      try:
        self.f = open(self.fname, 'r')
      except:
        raise FileNotFoundError(self.fname, 'cannot be opened')
        
    def next(self):
        with self.f:
            for row in self.f:
                line = row.strip().split(self.sep)
                if len(line) == self.num_of_args:
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
        
class StudentTest(unittest.TestCase):
    student = Student('104111', 'Rafif, A', 'SSW')
    def test_init(self):
        self.assertEqual(StudentTest.student.CWID, '104111')
        self.assertEqual(StudentTest.student.name, 'Rafif, A')
        self.assertEqual(StudentTest.student.major, 'SSW')
        
    def test_get_values_and_std_course(self):
        self.assertEqual(StudentTest.student.std_course('SSW810', 'A'), {'SSW810': 'A'})
        self.assertEqual(StudentTest.student.std_course('SSW555', 'A'), {'SSW810': 'A', 'SSW555': 'A'})
        self.assertEqual(StudentTest.student.get_values(), {'Taken Courses': {'SSW555': 'A', 'SSW810': 'A'}, 
                                                                'Major': 'SSW', 'Name': 'Rafif, A'})
               
class InstructorTest(unittest.TestCase):
    instructor = Instructor('98111', 'Maha, A', 'SSW')
    def test_init(self):
        self.assertEqual(InstructorTest.instructor.CWID, '98111')
        self.assertEqual(InstructorTest.instructor.name, 'Maha, A')
        self.assertEqual(InstructorTest.instructor.department, 'SSW')
        
    def test_get_values_and_inst_course(self): 
        self.assertEqual(InstructorTest.instructor.inst_course('SSW810'), {'SSW810': 1})
        self.assertEqual(InstructorTest.instructor.inst_course('SSW555'), {'SSW810': 1, 'SSW555': 1})
        self.assertEqual(InstructorTest.instructor.inst_course('SSW555'), {'SSW810': 1, 'SSW555': 2})
        self.assertEqual(InstructorTest.instructor.get_values(), {'Taught Courses': {'SSW555': 2, 'SSW810': 1}, 
                                                                    'Department': 'SSW', 'Name': 'Maha, A'})
                                                                    
class FileReaderTest(unittest.TestCase):
    f = FileReader('/Users/rafifarab/Desktop/Stevens/Fall 2017/SSW 810/students.txt', 3)
    def test_init(self):
        self.assertRaises(FileNotFoundError, FileReader.__init__, FileReaderTest.f, 
                            '/Users/rafifarab/Desktop/Stevens/Fall 2017/SSW 810/w.txt', 3)
        
if __name__ == '__main__':
        main(), unittest.main(exit = False, verbosity = 2)                                             