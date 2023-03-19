"""database

Revision ID: 8cd89d3ae90e
Revises: 
Create Date: 2023-03-18 12:21:15.281995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8cd89d3ae90e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_title', sa.String(length=80), nullable=False),
    sa.Column('course_code', sa.String(length=20), nullable=False),
    sa.Column('course_unit', sa.Integer(), nullable=False),
    sa.Column('tutor_name', sa.String(length=80), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_code'),
    sa.UniqueConstraint('course_title')
    )
    op.create_table('students',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=50), nullable=False),
    sa.Column('last_name', sa.String(length=50), nullable=False),
    sa.Column('password_hash', sa.Text(length=50), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('student_id', sa.String(length=20), nullable=True),
    sa.Column('gpa', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('student_id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('password_hash', sa.Text(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('student_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_code', sa.String(length=20), nullable=False),
    sa.Column('course_unit', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(precision=10), nullable=True),
    sa.Column('grade', sa.String(length=10), nullable=True),
    sa.Column('first_name', sa.String(length=80), nullable=False),
    sa.Column('last_name', sa.String(length=80), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_code')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('student_courses')
    op.drop_table('users')
    op.drop_table('students')
    op.drop_table('courses')
    # ### end Alembic commands ###