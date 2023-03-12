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
    tutor_id = db.Column(db.String, db.ForeignKey('tutors.id'))
    # date_created = db.Column(db.Datetime(), default=datetime.utcnow)



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
    
    



# Handles courses for each student
class StudentCourse(db.Model):
    __tablename__ = 'student_courses'

    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    # date_created = db.Column(db.Datetime(), default=datetime.utcnow)


    # @classmethod
    # def get_courses_by_student_id(cls, student_id):
    #     courses = Course.query\
    #         .join(StudentCourse, StudentCourse.course_id == Course.id)\
    #         .join(Student, Student.id == StudentCourse.student_id)\
    #         .filter(Student.id == student_id).all()
        
    #     return courses

    # using the database
    # @classmethod
    # def get_students_in_course_by(cls, course_id):
    #     students = Student.query\
    #         .join(StudentCourse, StudentCourse.student_id == Student.id)\
    #         .join(Course, Course.id == StudentCourse.course_id)\
    #         .filter(Course.id == course_id).all()
        
        # return students

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

    id = db.Column(db.Integer(), primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), primary_key=True)
    score = db.Column(db.Float(10), nullable=True)
    percent = db.Column(db.String(10), nullable=True)
    gpa = db.Column(db.Float(10))
    # date_created = db.Column(db.Datetime(), default=datetime.utcnow)


    @classmethod
    def __init__(self, student_id, course_id, score):
        self.student_id = student_id
        self.course_id = course_id
        self.score = score
    
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
    

