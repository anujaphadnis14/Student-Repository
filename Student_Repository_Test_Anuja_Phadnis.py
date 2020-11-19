""" Testing all functions of file Student_Repository_Anuja_Phadnis using unittest """
import unittest
from Student_Repository_Anuja_Phadnis import Student, Instructor, University, Major

class TestRepository(unittest.TestCase):
    """To verify University data repository"""    
    
    def test_University(self) -> None:
        """ To verify the student, Major and instructor details"""
        
        uni_data: University = University("E:/stevens/SSW 810 Python/Programs & Assignments/Stevens")
        
        student_data = {cwid: student.student_info() for cwid, student in uni_data.students.items()}
        
        expected_studdata = {'10103': ['10103', 'Baldwin, C', 'SFEN', ['CS 501', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.44],
                    '10115': ['10115', 'Wyatt, X', 'SFEN', ['CS 545', 'SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], [], 3.81], 
                    '10172': ['10172', 'Forbes, I', 'SFEN', ['SSW 555', 'SSW 567'], ['SSW 540', 'SSW 564'], ['CS 501', 'CS 513', 'CS 545'], 3.88], 
                    '10175': ['10175', 'Erickson, D', 'SFEN', ['SSW 564', 'SSW 567', 'SSW 687'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 513', 'CS 545'], 3.58], 
                    '10183': ['10183', 'Chapman, O', 'SFEN', ['SSW 689'], ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'],['CS 501', 'CS 513', 'CS 545'], 4.0], 
                    '11399': ['11399', 'Cordova, I', 'SYEN', ['SSW 540'], ['SYS 612', 'SYS 671', 'SYS 800'], [], 3.0], 
                    '11461': ['11461', 'Wright, U', 'SYEN', ['SYS 611', 'SYS 750', 'SYS 800'], ['SYS 612', 'SYS 671'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.92],
                    '11658': ['11658', 'Kelly, P', 'SYEN', [], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 0], 
                    '11714': ['11714', 'Morton, A', 'SYEN', ['SYS 611', 'SYS 645'], ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810'], 3.0], 
                    '11788': ['11788', 'Fuller, E', 'SYEN', ['SSW 540'],['SYS 612', 'SYS 671', 'SYS 800'], [], 4.0] }
        
        self.assertEqual(student_data, expected_studdata)

        major_data = {major: maj.major_info(maj) for major, maj in uni_data.majors.items()}
        expected = {
            'SFEN': ['SFEN', ['SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'] ,['CS 501', 'CS 513', 'CS 545']],
            'SYEN': ['SYEN', ['SYS 612', 'SYS 671', 'SYS 800'], ['SSW 540', 'SSW 565', 'SSW 810']]}
        self.assertEqual(expected, major_data)
    
        

if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
