from ..utils import db
from enum import Enum
from datetime import datetime
from werkzeug.security import generate_password_hash


# enum for enrollment_status
# class EnrollmentStatus(db.Enum):
#     WAIT_LISTED = 'wait_listed'
#     ENROLLED = 'enrolled'
#     DROPPED = 'dropped'



# Base class that other users can inherit from using the polymorphic hierarchy
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text, nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)


    def __repr__(self):
        return f"<User {self.username}>"

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
    
    
def hash_password(password):
    return generate_password_hash(password, method='sha256')




# A student class inheriting from the base class (User)
class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.Text(50), nullable=False, default=hash_password("Student101"))
    email = db.Column(db.String(80), nullable=False, unique=True)
    # enrollment_status = db.Column(db.Enum(EnrollmentStatus), default=EnrollmentStatus.WAIT_LISTED)
    student_id = db.Column(db.String(20), unique=True)
    gpa = db.Column(db.Float, default=0.0)
    registered_courses = db.relationship('StudentCourse', lazy=True, backref='StudentCourse.id')

    # Add ForeignKey constraint
    # registered_courses_fk = db.Column(db.Integer(), db.ForeignKey('student_courses.id'))


    def __repr__(self):
        return f"<Student {self.username}>"
    
    
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
    


# The Tutor class inheriting from the base class(User)
# class Tutor(db.Model):
#     __tablename__ = 'tutors'

#     id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
#     tutor_name = db.Column(db.String(20), nullable=False, unique=True)
#     courses = db.relationship('Course', backref='tutor_courses')
#     # grades = db.relationship('Grade', backref='tutor_grades', lazy=True)


    # def __repr__(self):
    #     return f"<Tutor {self.username}>"
    
    # def save(self):
    #     db.session.add(self)
    #     db.session.commit()

    # def update(self):
    #     db.session.commit()

    # def delete(self):
    #     db.session.delete(self)
    #     db.session.commit()

    # @classmethod
    # def get_by_id(cls, id):
    #     return cls.query.get_or_404(id)
    

    

