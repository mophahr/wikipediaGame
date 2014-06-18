wikipediaGame
=============

Installation
------------

We install Django

     pip install django

and then initialise the database: In the directory (wikipediaGame) run
     
     python manage.py syncdb
and that's *almost* it.

If you're running the server for the first time or after a long while again please run the subcategory crawler first:

     cd ./wikigame
     python subcategory_crawler.py
to build up the lists of allowed subcategories. **NOTE: THIS MAY TAKE SEVERAL MINUTES!**


Running the server
------------------

Go to the directory (wikipediaGame) and run

     python manage.py runserver

Enter the url `127.0.0.1:8000` In you browser of choice. It should be there.
