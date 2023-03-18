from ..utils import db
from datetime import datetime
from ..models.user import Student


# Handles courses for each tutor




# Courses model
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer(), primary_key=True)
    course_title = db.Column(db.String(80), nullable=False, unique=True)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    course_unit = db.Column(db.Integer(), nullable=False)
    tutor_name = db.Column(db.String, db.ForeignKey('tutors.tutor_name'))

    date_created = db.Column(db.DateTime(), default=datetime.utcnow)



    def __repr__(self):
        return f"<Course {self.course_code}>"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    
    



# Establishes a relationship between the students and courses table
class StudentCourse(db.Model):
    __tablename__ = 'student_courses'

    id = db.Column(db.Integer(), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))


    
    def __repr__(self):
        return f"<Course {self.course_id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    



# Handles grades for each course
class Score(db.Model):
    __tablename__ = 'scores'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    score = db.Column(db.Float(10), nullable=True)
    # grade = db.Column(db.String(10), nullable=True)
    # date_created = db.Column(db.Datetime(), default=datetime.utcnow)


    # @classmethod
    # def __init__(self, student_id, course_id, score):
    #     self.student_id = student_id
    #     self.course_id = course_id
    #     self.score = score
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    


    def grades(self): {
        'A': '90-100',
        'B': '80-89',
        'C': '70-79',
        'D': '60-69',
        'F': '0-59'
    }


    def calculate_grades(self):
        if self.score >= 90:
            return 'A'
        elif self.score >= 80:
            return 'B'
        elif self.score >= 70:
            return 'C'
        elif self.score >= 60:
            return 'D'
        else:
            return 'F'
    
    def calculate_grade_points(grade, credits):
        if grade == "A":
            return 4.0 * credits
        elif grade == "B":
            return 3.0 * credits
        elif grade == "C":
            return 2.0 * credits
        elif grade == "D":
            return 1.0 * credits
        else:
            return 0.0 * credits
        

    def total_grade_points(score, credits):
        grade = calculate_grades(score)
        grade_points = calculate_grade_points(grade, credits)
        return grade_points * credits
        

    
    
    

