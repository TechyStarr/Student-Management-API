# Student-Management-API

Note: More functionalities will be implemented with time as it is still under development

## Table of Contents

- [Student Management Student](#student-management-student)
  - [Table of Contents](#table-of-contents)
  - [Live ( deployed version )](#live--deployed-version-)
  - [Testing Locally](#testing-locally)
  - [Available Endpoint](#available-endpoint)
    - [Auth Endpoint](#auth-endpoint)
    - [Students Endpoint](#students-endpoint)
    - [Courses Endpoint](#courses-endpoint)

## Live ( deployed version ) 

Visit [website](http://olakaycoder1.pythonanywhere.com/)
## Testing Locally

Clone the repository


```console
git clone https://github.com/TechyStarr/Student-Management-API.git
```



Change directory to the cloned folder

```console
cd student-mgt
```

Install necessary dependency to run the project

```console
pip install -r requirements.txt
```
Create database from migration files 

```console
flask db migrate -m "your description"
```

```console
flask db upgrade
```
Run application

```console
flask run
```





## Available Endpoint

### Auth Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `auth/register` | _POST_ | It allows an admin to create an account  | Any | Any |  ---- | 
|  `auth/token` |  _POST_  | Generates an access and refresh token for user authentication | Any | Any | ---- | 
|  `auth/token/refresh` |  _POST_  | It is used to refresh expired tokens   | Authenticated | Any | ---- | 



### Students Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `students` |  _GET_  | It allows the retrieval all student is the school   | Authenticated | Admin | ---- |
|  `students/<student_id>` |  _GET_  | It allows the  retrieval of a student | Authenticated | Any | A student ID |
|  `students/<student_id>/courses/grade` |  _GET_  | It allows the retrieval a student all courses grade   | Authenticated | Any | A student ID |
|  `students/<student_id>/courses` |  _GET_  | It allows the retrieval of a student courses   | Authenticated | ---- | A student ID |
|  `students/<student_id>/gpa` |  _GET_  | Calculate a student gpa score   | Authenticated | Any | A student ID |
|  `students/courses/add_and_drop` |  _POST_  | It allows student register a course   | Authenticated | Student | ---- |
|  `students/courses/add_and_drop` |  _DELETE_  | It allows student unregister a course   | Authenticated | Student | ---- |
|  `students/course/add_score` |  _PUT_  | It allow teacher add a student score in a course | Authenticated | Teacher | ---- |


### Courses Endpoint
| ROUTE | METHOD | DESCRIPTION | AUTHORIZATION  | USER TYPE |  PLACEHOLDER | 
| ------- | ----- | ------------ | ------|------- | ----- |
|  `courses` |  _GET_  | It allows the retrieval of all available courses   | Authenticated | Any | ---- |
|  `courses` |  _POST_  | It allows the creation of a new course   | Authenticated | Admin | ---- |
|  `courses` |  _DELETE_  | It allows deleting a course   | Authenticated | Admin | ---- |
|  `courses/<course_id>` |  _GET_  | It allows the retrieval all student is the school   | Authenticated | Admin | A course ID |
|  `courses/<course_id>/students` |  _GET_  | It allows the  retrieval of all students in a courses | Authenticated | Any | A course ID |
|  `courses/<course_id>/students/add_and_drop` |  _POST_  | It allows teacher add a  student the their course | Authenticated | Teacher | A course ID |
|  `courses/<course_id>/students/add_and_drop` |  _DELETE_  | It allows teacher remove a  student from their course | Authenticated | Teacher | A course ID |
|  `courses/grade` |  _GET_  | It allows student retrieve all registered courses grade | Authenticated | Student | ---- |


