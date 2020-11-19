""" 
    SSW 810 Homework 10
    Name: Anuja Phadnis
    Purpose: To create a data repository for students, instructors and courses
             To display completed courses, remaining courses and Student's GPA
    CWID:10446233
    Date: 11/18/2020
"""

#importing necessary libraries
from typing import List, Dict, DefaultDict, Tuple, Optional, Iterator, IO, Set

import os
from os import listdir
from prettytable import PrettyTable
from collections import defaultdict

class Major:
    """To store the courses related to major"""
    
    pretty_table: Tuple[str, str, str] = ("Major", "Required Courses", "Electives") 

    def __init__(self, major: str, req_or_ele: str, course: str)-> None:
        """ Initializing the variables of Class Major"""

        self.major: str = major
        self.req_courses: Set[str] =set()
        self.ele_courses: Set[str] =set()
        self.add_course_major(req_or_ele,course)

    def add_course_major(self, req_or_ele: str, course: str)-> None:
        """ Adding the required and elective courses based on major"""

        if(req_or_ele == 'R'):
            self.req_courses.add(course)
        elif(req_or_ele == 'E'):
            self.ele_courses.add(course)
        else:
            print("Please provide wether the course is req or elective")
    
    def major_info(self,major: str)-> Tuple[str, Set[str], Set[str]]:
        """ Returning the major, required, elective courses"""

        return [self.major, sorted(self.req_courses), sorted(self.ele_courses)]

class Student:
    """To store all information about every student"""

    def __init__(self,cwid: str, name: str, major: str)-> None:
        """Initializing the variables for student class"""

        self.cwid:str = cwid
        self.name: str = name
        self.major: str = major
        self.passed_courses: Set[str] = set()
        self.rem_req_courses: Set[str] = set()
        self.rem_ele_courses: Set[str] = set()
        self.gpa : float = 0.0
        self.allocated_grades:Dict[str, str]  = {}
        self.passing_grades: Set[str] = set(['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C' ])
        self.grades_to_gpa: Dict[str] = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-':2.75, 'C+': 2.25, 'C': 2.0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0}
        
    def add_grade(self, course: str, grade: str) -> None:
        """Adding grade for a course for a student""" 

        self.allocated_grades[course] = grade
        
        if grade in self.passing_grades:
            self.passed_courses.add(course)
            if course in self.rem_req_courses:
                self.rem_req_courses.remove(course)
            if course in self.rem_ele_courses:
                self.rem_ele_courses.remove(course)
    
    def remaining_courses(self, major: Major)->None:
        """ Determining remaining courses""" 

        self.rem_req_courses = major.req_courses - self.passed_courses
        
        #Checking for the remaining elective courses
        if(len(self.passed_courses.intersection(major.ele_courses)) ==0 ):
            self.rem_ele_courses = major.ele_courses - self.passed_courses
    
    def calculate_gpa(self) -> None:
        """ Function to calculate gpa for the courses """

        sum: float = 0.0
        
        if(len(self.passed_courses)>0):
            for course in self.passed_courses:
                sum = sum + self.grades_to_gpa[self.allocated_grades[course]]
            
            self.gpa  = float(sum) / float(len(self.passed_courses))
        else:
            self.gpa = 0.0
    
    def student_info(self)-> Tuple[str, str, List[str]]:
        """Returning student info: cwid,name,major,passed courses etc"""
        
        return [self.cwid, self.name,self.major,sorted(self.passed_courses),sorted(self.rem_req_courses),sorted(self.rem_ele_courses),round(self.gpa,2)]

class Instructor:
    """To store all information about every instructor"""

    pretty_table: List[str] = ["CWID", "Name", "Dept", "Course", "Students"] 

    def __init__(self,cwid: str, name: str, department: str)-> None:

        """Initializing the instructor variables"""

        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self.courses_head_count: DefaultDict[str,int] = defaultdict(int) 

    def add_course(self, course: str)-> None:
        """ Adding and updating the course and the number of students who have taken the course"""
        
        self.courses_head_count[course] += 1 
    
    def instructor_info(self,course: Optional[str] = None)-> Tuple[str, str, List[str]]:
        """ Returning the information to be printed in pretty table """
        
        no_of_students = self.courses_head_count[course]
        
        return [self.cwid, self.name, self.department, course, no_of_students ]


class University:
    """Holds all of  the students, instructors and grades for a single University"""
    
    def __init__(self, directory: Optional[str]=None) -> None:
        """ Initializing the University"""

        self.directory: str = directory 
        self.students: Dict[str, Student] = dict() 
        self.instructors: Dict[str, Instructor] = dict()
        self.majors: Dict[str, Major] = dict()

        if directory != None:
            self.check_validity(directory)
            self.populate_major()
            self.populate_instructor()
            self.populate_students()
            self.populate_grades()
            self.populate_rem_courses()
            self.populate_gpa()
        
    def print_pretty_tables(self) -> None:
        """ To print all the pretty table"""
        
        print("Major Info")
        self.pretty_print_major()

        print("Student Info")
        self.pretty_print_students()

        print("Instructor Info")
        self.pretty_print_instructor()
    
    def check_validity(self,directory:str)-> None:
        """ Validating the directory"""

        try:
            files: list = listdir(directory)
        except FileNotFoundError:
            raise FileNotFoundError("Error: The given directory is not found")
        except NotADirectoryError:
            raise NotADirectoryError("Error: The given path is not a valid directory")

        if not 'students.txt' in files:
            raise FileNotFoundError("Error: students.txt file not found")
        
        if not 'grades.txt' in files:
            raise FileNotFoundError("Error: grades.txt file not found")

        if not 'instructors.txt' in files:
            raise FileNotFoundError("Error: instructors.txt file not found")

        if not 'majors.txt' in files:
            raise FileNotFoundError("Error: majors.txt file not found ")
    
    def populate_rem_courses(self) ->None:
        """To populate remaining courses"""

        for student in self.students.values():
            student.remaining_courses( self.majors[student.major])
    
    def populate_major(self) -> None:
        """ Storing the major info"""
        
        for major, req_or_ele, course in self.file_reader(os.path.join(self.directory, "majors.txt"), 3, "\t", True):
            if self.majors.__contains__(major):
                self.majors[major].add_course_major(req_or_ele,course)
            else:
                major_info = Major(major,req_or_ele,course)
                self.majors[major] = major_info
    
    def populate_instructor(self) -> None:
        """ To populate instructor info """

        for cwid, name, department in self.file_reader(os.path.join(self.directory, "instructors.txt"), 3, "|", True):
            if self.instructors.__contains__(cwid):
                print(f"Instructor CWID {cwid} is duplicate")
            else:
                self.instructors[cwid] = Instructor(cwid, name, department)
    
    def populate_students(self) -> None:
        """ To populate the student info"""
        
        for cwid, name, major in self.file_reader(os.path.join(self.directory, "students.txt"), 3, ";", True):
            if self.students.__contains__(cwid):
                print(f"Student CWID {cwid} is duplicate")
            else:
                self.students[cwid] = Student(cwid, name, major)
    
    def populate_grades(self) -> None:
        """ To populate the grades and update the student and instructor instances accordingly """
        
        for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self.directory, "grades.txt"), 4, "|", True):
            if self.valid_grade(student_cwid, instructor_cwid):
                self.students[student_cwid].add_grade(course, grade)
                self.instructors[instructor_cwid].add_course(course) 
                
    def populate_gpa(self)->None:
        """calculating gpa for each student """
        
        for student in self.students.values():
            student.calculate_gpa()

    def valid_grade(self,student_cwid: str, instructor_cwid: str ) -> bool:
        """ Checks if the student and instructor cwid is valid """
        
        if not self.students.__contains__(student_cwid):
            raise ValueError(f"Student with {student_cwid} is not present")
        if not self.instructors.__contains__(instructor_cwid):
            raise ValueError(f"Instructor with {instructor_cwid} is not present")      
        return True
    
    def file_reader(self, path:str, fields:int, sep:str, header:bool = False) -> Iterator[List[str]]:
        """Function to read a file"""

        #Checking for valid file path
        if type(path) != str:
            raise TypeError("Please enter a valid path")
        else:
            file_name: str = path

        try:
            fp: IO = open(file_name, 'r', encoding='utf-8')
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Can't open '{path}'")
        else:
            with fp:
                for offset, line in enumerate(fp):
                    line = line.rstrip('\n')
                    
                    if offset == 0 and header:
                        continue
                    elif len(line.split(sep)) == fields:
                        yield line.split(sep)
                    else:
                        raise ValueError(f"Error: line {offset+1} in {path} has {len(line.split(sep))} fields instead of {fields}")
            
            fp.close()

    def pretty_print_major(self)-> None:
        """ To print major info pretty table """

        print_pt: PrettyTable = PrettyTable(field_names=Major.pretty_table)
        
        for each_major in self.majors.values():
            print_pt.add_row(each_major.major_info(each_major))
        
        print(print_pt)
    
    
    def pretty_print_students(self) -> None:
        """ To print student info pretty table """

        print_pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name','Major','Completed Courses','Remaining Required','Remaining Electives','GPA'))
        
        for student in self.students.values():
            print_pt.add_row(student.student_info())
        
        print(print_pt)
    
    def pretty_print_instructor(self) -> None:
        """ To print instructor info pretty table """

        print_pt: PrettyTable = PrettyTable(field_names=('CWID', 'Name', 'Dept', 'Course', 'Students'))
        
        for instructor in self.instructors.values():
            for course in instructor.courses_head_count:
                print_pt.add_row(instructor.instructor_info(course))
        
        print(print_pt)

def main():
    """To verify the above methods"""

    try:
        uni = University('E:/stevens/SSW 810 Python/Programs & Assignments/Student Repository/Stevens')
        uni.print_pretty_tables()
    except Exception as e:
        print(e)
    
    cust_path =  str(input("Do you want to test for another directory? Yes/No: "))
    if cust_path == "Yes":
        dir_path = str(input("Enter the directory path:"))

        try:
            University(dir_path)
        except Exception as e:
            print(e)
    else:
        print("Thank You!")

if __name__ == '__main__':
    main()

