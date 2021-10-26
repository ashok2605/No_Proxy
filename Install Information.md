<pre>
Follow this commands:
/*make sure u install python intrepreter first*/
1.pip install virtualenvwrapper-win
2.mkvirtualenv ams
3.workon ams
4./*browse to that directory where u can see manage.py in project*/
5.python manage.py runserver
6./*install postgresql..https://www.postgresql.org/download/ and pgadmin4...https://www.pgadmin.org/download/*/
7.pip install pyscopg2
8.python manage.py makemigrations
9./*U will see a number like 0011*/
10.python manage.py sqlmigrate home (thatnumberabove)
11.python manage.py migrate
12.python manage.py runserver
13.python manage.py createsuperuser
14./*Create a superuser with details who acts as admin*/
/*After creating superuser*/
15.python manage.py runserver




Above things u have to do if u are doing it for first time,but later
u have to use these commands.
1.workon ams
2./*browse to that directory where u can see manage.py in project*/
3.python manage.py runserver

/*Copy that link u see in command prompt and paste it in browser*/
							




</pre>