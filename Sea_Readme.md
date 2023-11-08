1. pip install Flask PyMySQL SQLAlchemy Flask-SQLAlchemy session xlrd xlwt os xlutils Flask-Migrate

2. When you run the teamwork.py. firstly, you need to go to the http://127.0.0.1:5000/teacher to import the teacher account. 
Then you need to go to the http://127.0.0.1:5000/course to import the course information.
then you need to go the login page (http://127.0.0.1:5000/user/login)
input the teacher account(ben@uic.edu.hk, 123456)
select a course. 
then teacher can use every case.(generate student-> edit submission -> form team method -> student -> teacher-> calculate two thing -> export)
the important page is form team page. teacher need to input the number per group
And choose one method. 
And the export file is in your project file -> static/

For student. you need to input the student account. The default password is 0000. After login, student to update the password.
(student -> update password -> vote leader -> Another student -> vote leader -> evaluate  same leader -> leader login-> set contribution-> teacher)
student can see choose team member page, when teacher select method 1. 
