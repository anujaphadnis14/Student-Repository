""" 
    SSW 810 Homework 09
    Name: Anuja Phadnis
    Purpose: To create a data repository for students, instructors and courses
    CWID:10446233
    Date: 11/11/2020
"""

#importing necessary libraries
from typing import List, Dict, DefaultDict, Tuple, Optional, Iterator, IO
import os
from os import listdir
from prettytable import PrettyTable
from collections import defaultdict

class Student:
    """To store all information about every student"""
    pretty_table:Tuple[str, str, str] = ("CWID", "Name", "Completed Courses")

    def __init__(self, cwid: str, name: str, major: str) -> None:
        """Initializing the student variables"""

        self.cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self.courses: Dict[str, str] = dict() 
    
    def add_grade(self, course: str, grade: str) -> None:
        """Adding course grade for each student"""

        self.courses[course] = grade

    def student_info(self) -> List:
        """To retuen the summary of all the info of a student"""

        return [self.cwid, self.name, sorted(self.courses.keys())]

class Instructor:
    """To store all information about every instructor"""

    pretty_table: List[str] = ["CWID", "Name", "Dept", "Course", "Students"] 

    def __init__(self, cwid: str, name: str, department: str) -> None:
        """Initializing the instructor variables"""

        self.cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self.courses: DefaultDict[str, int] = defaultdict(int)

    def add_course(self, course_name: str) -> None:
        """ Adding and updating the course taught by instructor and the number of students who have taken the course """
        
        self.courses[course_name] += 1

    def instructor_info(self) -> Iterator[Tuple]:
        """ information returned to be printed in pretty table """
        
        for course, no_students in self.courses.items():
            yield (self.cwid, self.name, self.department, course, no_students)

class University:
    """Holds all of  the students, instructors and grades for a single University"""

    def __init__(self, directory, pretty_tables: bool=True) -> None:
        """Initializing the University with students and instructors"""
        
        self.directory: str = directory 
        self.students: Dict[str, Student] = dict() 
        self.instructors: Dict[str, Instructor] = dict() 
        
        if directory != None:
            self.check_validity(directory)
            self.populate_students()
            self.populate_instructor()
            self.populate_grades()
    

        if pretty_tables:
            print("Student summary")
            self.student_pretty_table()

            print("\nInstructor Summary")
            self.instructor_pretty_table()
    
    def check_validity(self,directory:str)-> None:
        """ Validation for the directory"""

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
    
    
    def populate_students(self) -> None:
        """ To populate the student info"""
        
        for cwid, name, major in self.file_reader(os.path.join(self.directory, "students.txt"), 3, "\t", False):
            if cwid in self.students:
                print(f"Student CWID {cwid} is duplicate")
            else:
                self.students[cwid] = Student(cwid, name, major)
    
    def populate_instructor(self) -> None:
        """ To populate instructor info """

        for cwid, name, department in self.file_reader(os.path.join(self.directory, "instructors.txt"), 3, "\t", False):
            if cwid in self.instructors:
                print(f"Instructor CWID {cwid} is duplicate")
            else:
                self.instructors[cwid] = Instructor(cwid, name, department)

    def populate_grades(self) -> None:
        """ To populate the grades and update the student and instructor instances accordingly """
        
        for student_cwid, course, grade, instructor_cwid in self.file_reader(os.path.join(self.directory, "grades.txt"), 4, "\t", False):
            if self.valid_grade(student_cwid, instructor_cwid):
                self.students[student_cwid].add_grade(course, grade)
                self.instructors[instructor_cwid].add_course(course)    
    
    def valid_grade(self,student_cwid: str, instructor_cwid: str ) -> bool:
        """ Checks if the student and instructor cwid is valid """
        
        if not self.students.__contains__(student_cwid):
            raise ValueError(f"Student with {student_cwid} is not present")
        if not self.instructors.__contains__(instructor_cwid):
            raise ValueError(f"Instructir with {instructor_cwid} is not present")      
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
        
    def student_pretty_table(self) -> None:
        """ To print student info pretty table """

        print_pt: PrettyTable = PrettyTable(field_names=Student.pretty_table)

        for stud in self.students.values():
            print_pt.add_row(stud.student_info())

        print(print_pt)

    def instructor_pretty_table(self) -> None:
        """ To print student info pretty table """

        print_pt: PrettyTable = PrettyTable(field_names=Instructor.pretty_table)

        for inst in self.instructors.values():
            for each_instructor in inst.instructor_info():
                print_pt.add_row(each_instructor)

        print(print_pt)

def main():
    """To verify the above methods"""

    try:
        University('E:/stevens/SSW 810 Python/Programs & Assignments/HW09_Anuja_Phadnis/Stevens')
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

