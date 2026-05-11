class AssessmentSystem:
    """
    This is a class as an student assessment system, which supports add student, add course score, calculate GPA, and other functions for students and courses.
    """

    def __init__(self):
        """
        Initialize the students dict in assessment system.
        """
        self.students = {}

    def add_student(self, name, grade, major):
        """
        Add a new student into self.students dict
        """
        self.students[name] = {
            'name': name,
            'grade': grade,
            'major': major,
            'courses': {}
        }

    def add_course_score(self, name, course, score):
        """
        Add score of specific course for student in self.students
        """
        if name in self.students:
            self.students[name]['courses'][course] = score

    def get_gpa(self, name):
        """
        Get average grade of one student.
        """
        if name in self.students and self.students[name]['courses']:
            scores = self.students[name]['courses'].values()
            return sum(scores) / len(scores)
        return None

    def get_all_students_with_fail_course(self):
        """
        Get all students who have any score blow 60
        """
        failed_students = []
        for name, data in self.students.items():
            for score in data['courses'].values():
                if score < 60:
                    failed_students.append(name)
                    break
        return failed_students

    def get_course_average(self, course):
        """
        Get the average score of a specific course.
        """
        total = 0
        count = 0
        for data in self.students.values():
            if course in data['courses']:
                total += data['courses'][course]
                count += 1
        return total / count if count > 0 else None

    def get_top_student(self):
        """
        Calculate every student's gpa with get_gpa method, and find the student with highest gpa
        """
        top_student = None
        max_gpa = -1
        for name in self.students:
            gpa = self.get_gpa(name)
            if gpa is not None and gpa > max_gpa:
                max_gpa = gpa
                top_student = name
        return top_student