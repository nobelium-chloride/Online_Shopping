# Basic clone of online-shopping but forked

coursera
stride-cohort-4

#This project is an extension of:
#Project - https://www.freecodecamp.org/news/structuring-a-flask-restplus-web-service-for-production-builds-c2ec676de563/
#Find original Repository here - https://github.com/cosmic-byte/flask-restplus-boilerplate


NB: - Some errors and how to fix:
--
1. **Target database is not up to date** --> This could happen if you had made chamged to db or db models.
$ python manage.py db stamp head
$ python manage db migrate -- message "<ENTER CHANGES YOU MADE TO DB>"
$ python manage db upgrade
  
