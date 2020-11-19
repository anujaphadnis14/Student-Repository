""" Testing all functions of file HW09_Anuja_Phadnis using unittest """
import unittest
from Student_Repository_Anuja_Phadnis import Student, Instructor, University

class TestRepository(unittest.TestCase):
    """To verify Student and Instructor data repository"""    
    
    def test_University(self) -> None:
        """ To verify the student and instructor repository """
        
        uni_data: University = University("E:/stevens/SSW 810 Python/Programs & Assignments/HW09_Anuja_Phadnis/Stevens")
        
        student_data = {cwid: student.student_info() for cwid, student in uni_data.students.items()}
        
        expected_studdata = {'10103': ['10103','Baldwin, C',['CS 501','SSW 564', 'SSW 567', 'SSW 687']],
                    '10115': ['10115','Wyatt, X',['CS 545','SSW 564', 'SSW 567', 'SSW 687']],
                    '10172': ['10172','Forbes, I',['SSW 555', 'SSW 567']],
                    '10175': ['10175','Erickson, D',['SSW 564', 'SSW 567', 'SSW 687']],
                    '10183': ['10183','Chapman, O',['SSW 689']],
                    '11399': ['11399','Cordova, I',['SSW 540']],
                    '11461': ['11461','Wright, U',['SYS 611','SYS 750', 'SYS 800']],
                    '11658': ['11658','Kelly, P',['SSW 540']],
                    '11714': ['11714','Morton, A',['SYS 611','SYS 645']],
                    '11788': ['11788','Fuller, E',['SSW 540']]}
        
        self.assertEqual(student_data, expected_studdata)
        
        instructor_data = {tuple(each_instructor) for inst in uni_data.instructors.values() for each_instructor in inst.instructor_info()}
        
        expected_instdata = {('98765', 'Einstein, A', 'SFEN', 'SSW 567', 4),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 564', 3),
                    ('98765', 'Einstein, A', 'SFEN', 'SSW 540', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'SSW 687', 3),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 501', 1),
                    ('98764', 'Feynman, R', 'SFEN', 'CS 545', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 555', 1),
                    ('98763', 'Newton, I', 'SFEN', 'SSW 689', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 800', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 750', 1),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 611', 2),
                    ('98760', 'Darwin, C', 'SYEN', 'SYS 645', 1)}
        
        self.assertEqual(instructor_data, expected_instdata)

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)