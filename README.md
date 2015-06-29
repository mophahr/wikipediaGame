wikipediaGame
=============

Installation
------------

Install pip if you don't have it:

    wget "https://bootstrap.pypa.io/get-pip.py"
    python get-pip.py

(Optional) create a virtualenv and enter into it

     # install virtualenv if necessary:
     pip install virtualenv

     # create a virtual environment
     virtualenv ~/.virtualenvs/wikigame

     # switch to it:
     source ~/.virtualenvs/wikigame/bin/activate

Install Django:

     pip install django

Clone the code:

    git clone https://github.com/mophahr/wikipediaGame.git

Initialise the database: In the directory (wikipediaGame) run

     cd wikipediaGame
     mkdir database
     python manage.py migrate

and that's it.

Running the game
----------------

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





