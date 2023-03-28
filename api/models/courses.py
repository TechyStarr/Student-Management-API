from ..utils import db
from datetime import datetime
from ..models.user import Student


# Handles courses for each tutor




# Courses model
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer(), primary_key=True)
    course_title = db.Column(db.String(80), nullable=False)
    course_code = db.Column(db.String(20), nullable=False, unique=True)
    course_unit = db.Column(db.Integer(), nullable=False)
    tutor_name = db.Column(db.String(80), nullable=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    # registered_courses = db.relationship('StudentCourse', lazy=True, backref='registered_courses')
    # registered_student = db.relationship('StudentCourse', lazy=True, viewonly=True, overlaps='course, registered_courses', backref='registered_student')



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
    course_code = db.Column(db.String(20), nullable=False)
    course_unit = db.Column(db.Float(10), nullable=False)
    score = db.Column(db.Float(2), default=0.0)
    grade = db.Column(db.String(2), default='N/A')
    student_id = db.Column(db.Integer(), db.ForeignKey('students.id'))


    

    
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
    




def calculate_grades(score):
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
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

def calculate_gpa(score, credits):
    total_grade_points = total_grade_points(score, credits)
    gpa = total_grade_points / credits
    return gpa


