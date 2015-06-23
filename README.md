wikipediaGame
=============

Installation
------------
If you are on python 2 switch to a python 3 environment:
     
     # install virtualenv if necessary:
     pip install virtualenv
     
     # create an environment called Py3VE:
     virtualenv -p python3 envname
     
     # switch to it:
     source Py3VE/bin/activate
     
We install Django

     pip install django

and then initialise the database: In the directory (wikipediaGame) run
     
     mkdir database
     python manage.py syncdb

and that's it.

Running the server
------------------

Go to the directory (wikipediaGame) and run

     python manage.py runserver

Enter in the browser in the url `127.0.0.1:8000`. It should be it.

Translations
------------

To update translations, run

	python manage.py makemessages -l de

this updates the file located at 

	locale/de/LC_MESSAGES/django.po

which can be modified to translate the website.





