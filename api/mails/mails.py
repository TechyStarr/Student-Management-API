import smtplib
from email.mime.text import MIMEText
from ..models.user import User, Student, Admin, Tutor

def send_mail(user_id, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('email', 'password')

    msg = MIMEText(f"Dear {user_id.name}, \n\n"
                    f"Welcome to Starr Learning. \n\n"
                    f"Your student ID is {user_id.id} \n\n"
                    f"Your password is {password} \n\n"
                    f"Please log in to the student portal with the above details to access your account. /n"
                    f"Thank you. \n\n"
                    f"Regards, \n"
                    f"Starr Learning Team")
    
    msg['Subject'] = 'Congratulations!'
    msg['From'] = 'admin@starrlearning.edu'
    msg['To'] = user_id.email


