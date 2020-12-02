
""" Testing all functions of file Student_Repository_Anuja_Phadnis using unittest """
import unittest
from typing import Tuple, List
from Student_Repository_Anuja_Phadnis import Student, Instructor, University, Major

class Test_Student(unittest.TestCase):
    """ To verify the methods from class Student"""

    def test_add_grade(self)-> None:
        """ To verify add_grade method"""

        st = Student('10446233', 'Anuja', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('CS-601-A', 'A-')
        st.add_grade('SSW-800-B', 'A')
        st.add_grade('CS-590-A', 'D')

        self.assertEqual(len(st.allocated_grades), 4)
        self.assertEqual(len(st.passed_courses), 3)
        self.assertEqual(st.allocated_grades['CS-601-A'], 'A-')
    
    def test_remaining_courses(self)-> None:
        """ To verify add_remaining method"""
        
        mj = Major('CS', 'R' , 'CS-509')
        mj.add_course_major('R', 'Python')
        mj.add_course_major('E', 'Finance')
        mj.add_course_major('E', 'Statistics')
        mj.add_course_major('R', 'Data Structures')

        st = Student('10446233', 'Anuja', 'CS')
        st.remaining_courses(mj)
        
        self.assertEqual(len(st.rem_ele_courses), 2)
        self.assertEqual(len(st.rem_req_courses), 3)
    
    def test_calculate_gpa(self)->None:
        """ To verify calculate_gpa method """

        st = Student('10446233', 'Anuja', 'Computer_Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-800-C', 'A-')
        st.add_grade('CS-590-A', 'A')
        st.add_grade('CS-510-B', 'D')
     
        st.calculate_gpa()     

        self.assertEqual(round(st.gpa,2),3.92)
    
    def test_student_info(self) -> None:
        """ To verify student_info method"""
        
        st = Student('10446233', 'Anuja', 'Computer Science')
        st.add_grade('SSW-810-A', 'A')
        st.add_grade('SSW-800-A', 'A-')

        st_tuple: Tuple = st.student_info()

        self.assertEqual(st_tuple[0],'10446233')
        self.assertEqual(st_tuple[1],'Anuja')
        self.assertEqual(st_tuple[2],'Computer Science')

class Test_Instructor(unittest.TestCase):
    """ To verify the methods in from class Instructor """

    def test_add_course(self)-> None:
        """ To test add_course method"""

        inst = Instructor('1112343', 'Prof.Raz', 'SSW')
        inst.add_course('Python')
        inst.add_course('Software Testing')
        inst.add_course('Agile')

        self.assertEqual(inst.courses_head_count['Agile'], 1)
        self.assertEqual(inst.courses_head_count['Python'], 1)
        self.assertEqual(inst.courses_head_count.__contains__('Key'), False )

    def test_intstructor_info(self) -> None:
        """ To verify intsructor_info method"""

        inst = Instructor('10119444', 'Prof Raz', 'SSW')
        inst.add_course('Python')
        inst.add_course('Software Testing')
        inst.add_course('Agile')

        inst_tuple: Tuple = inst.instructor_info('Python')

        self.assertEqual(inst_tuple[0],'10119444')

class Test_Major(unittest.TestCase):
    """to verify the methods from class Major"""

    def test_add_course_major(self) -> None:
        """ to verify add_course_major method """

        mjr = Major('CS', 'R', 'SSW 810')
        mjr.add_course_major('R', 'SSW 811')
        mjr.add_course_major('E', 'MIS 636')

        self.assertEqual(len(mjr.req_courses), 2)
        self.assertEqual(len(mjr.ele_courses), 1)

    def test_major_info(self) -> None:
        """ To verify major_info method"""
        
        mjr = Major('ENV', 'R', 'ENV 546')
        mjr.add_course_major('R', 'ENV 610')
        mjr.add_course_major('E', 'SSW 600')
        
        major_tuple: Tuple = mjr.major_info('ENV')
        
        self.assertEqual(major_tuple[0],'ENV')

class Test_University(unittest.TestCase):
    """ To verify the methods from class University """


    def test_check_validity(self)-> None:
        """ To verify the method check_validity"""

        uni = University()

        with self.assertRaises(FileNotFoundError): uni.check_validity('./Something')
        with self.assertRaises(NotADirectoryError): uni.check_validity('./Student_Repository_Anuja_Phadnis.py')
    
    def test_student_grades_table_db(self) -> None:
        """ To verify student_grades_table_db method"""

        uni = University()
        student_grade: List = []
        for grade_info in  uni.student_grades_table_db("E:/stevens/SSW 810 Python/Programs & Assignments/Student Repository/810_startup.db"):
            student_grade.append(grade_info)

        self.assertEqual(len(student_grade),9)
        self.assertEqual(student_grade[0][1], '10115')
        self.assertEqual(student_grade[8][1], '10183')
    
    def test_populate_grades(self)-> None:
        """ To verify populate_grades method """

        uni = University('E:/stevens/SSW 810 Python/Programs & Assignments/Student Repository/Stevens')        
        uni.populate_students()
        uni.populate_instructor()
        uni.populate_grades()
        uni.populate_major()
        
        self.assertEqual(len(uni.students['10103'].allocated_grades), 2)
        self.assertEqual(uni.students['10103'].allocated_grades['CS 501'], 'B')
        self.assertEqual(len(uni.instructors['98764'].courses_head_count), 1)
        self.assertEqual(uni.instructors['98764'].courses_head_count['SYS 611'], 0)
       
    
        

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)