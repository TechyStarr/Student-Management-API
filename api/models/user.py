from ..utils import db
from datetime import datetime
from decouple import config
from itsdangerous import TimedSerializer as Serializer


# enum for enrollment_status
class EnrollmentStatus(db.Enum):
    WAIT_LISTED = 'wait_listed'
    ENROLLED = 'enrolled'
    DROPPED = 'dropped'



# Base class that other users can inherit from using the polymorphic hierarchy
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.Text(100), nullable=False)
    user_type = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean(), default=False)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)

    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'user'
    }



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
    
    



# For Admin User
class Admin(User):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nomination =db.Column(db.String(250))


    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }

    def __repr__(self):
        return f"<Admin {self.username}>"
    
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
    



# A student class inheriting from the base class (User)
class Student(User):
    __tablename__ = 'students'

    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    # enrollment_status = db.Column(db.Enum(EnrollmentStatus), default=EnrollmentStatus.WAIT_LISTED)
    matric_no = db.Column(db.String(20), unique=True)
    courses = db.relationship('Course', secondary='student_courses')
    score = db.relationship('Score', backref='student_score', lazy=True)


    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

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
class Tutor(User):
    __tablename__ = 'tutors'

    id = db.Column(db.Integer(), db.ForeignKey('users.id'), primary_key=True)
    tutor_no = db.Column(db.String(20), nullable=False, unique=True)
    courses = db.relationship('Course', backref='tutor_courses')
    # grades = db.relationship('Grade', backref='tutor_grades', lazy=True)


    __mapper_args__ = {
        'polymorphic_identity': 'tutor'
    }

    def __repr__(self):
        return f"<Tutor {self.username}>"
    
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
    

    

