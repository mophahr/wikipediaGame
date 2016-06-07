# -*- coding: utf-8 -*-
from django.db import models


class Problem(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    start = models.CharField(max_length=254)
    end = models.CharField(max_length=254)


class Result(models.Model):
    time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey('Problem')
    path_length = models.IntegerField()
    path = models.TextField()


def create_problems():
	"""
	Function to populate the db
	"""
	# easy
	#=====
	Problem.objects.get_or_create(id=1, start='Jogi Löw', end='Angela Merkel')
	Problem.objects.get_or_create(id=2, start='John Lennon', end='Michael Jackson')
	Problem.objects.get_or_create(id=3, start='Jean-Claude van Damme', end='Arnold Schwarzenegger')
	
	#normal
	#=====
	
	#dresden
	Problem.objects.get_or_create(id=8, start='August der Starke', end='Barack Obama')
	Problem.objects.get_or_create(id=9, start='Erich Kästner', end='Otto Dix')
	Problem.objects.get_or_create(id=19, start='Jan Josef Liefers', end='Jeff Goldblum')
	Problem.objects.get_or_create(id=29, start='Gerhard Richter', end='Max Planck')
	
	#sports
	Problem.objects.get_or_create(id=14, start='Silvia Neid', end='Marie Curie')
	Problem.objects.get_or_create(id=5, start='Kevin Großkreutz', end='Angela Merkel')
	Problem.objects.get_or_create(id=28, start='Lionel Messi', end='Elton John')
	Problem.objects.get_or_create(id=25, start='Venus Williams', end='Winston Churchill')
	Problem.objects.get_or_create(id=33, start='Martin Luther', end='Martina Navrátilová')
	
	#science
	Problem.objects.get_or_create(id=4, start='Albert Einstein', end='Michael Jackson')
	Problem.objects.get_or_create(id=11, start='Emmy Noether', end='Alfred Nobel')
	Problem.objects.get_or_create(id=22, start='Ada Lovelace', end='Jay Z')
	Problem.objects.get_or_create(id=34, start='Edwin Hubble', end='Aristarchos von Samos')
	Problem.objects.get_or_create(id=35, start='Richard Wagner', end='Richard Feynman')
	
	#entertainment
	Problem.objects.get_or_create(id=21, start='Tilda Swinton', end='Nicolas Cage')
	Problem.objects.get_or_create(id=10, start='Donald Duck', end='Albert Camus')
	Problem.objects.get_or_create(id=17, start='Udo Jürgens', end='Alexis Tsipras')
	Problem.objects.get_or_create(id=20, start='Ridley Scott', end='David Hasselhoff')
	Problem.objects.get_or_create(id=23, start='Miley Cyrus', end='Allen Ginsberg')
	
	#arts 
	Problem.objects.get_or_create(id=7, start='Johann Wolfgang von Goethe', end='Arnold Schwarzenegger')
	Problem.objects.get_or_create(id=15, start='Clara Schumann', end='Nina Hagen')
	Problem.objects.get_or_create(id=16, start='Franz Kafka', end='Franz Beckenbauer')
	Problem.objects.get_or_create(id=26, start='Virginia Woolf', end='Pamela Anderson')
	
	
	#history
	Problem.objects.get_or_create(id=12, start='Kleopatra VII.', end='Joachim Gauck')
	Problem.objects.get_or_create(id=13, start='Gaius Iulius Caesar', end='Roland Kaiser')
	Problem.objects.get_or_create(id=31, start='Jules Verne', end='Juri Alexejewitsch Gagarin')
	Problem.objects.get_or_create(id=30, start='Dionysos', end='Margot Honecker')


	#Problem.objects.get_or_create(id=36, start='', end='')

	
	#ignore:
	"""
	Problem.objects.get_or_create(id=6, start='Angela Merkel', end='Kevin Großkreutz')
	Problem.objects.get_or_create(id=18, start='Conchita Wurst', end='Wladimir Wladimirowitsch Putin')
	Problem.objects.get_or_create(id=27, start='Wladimir Putin', end='Conchita Wurst')
	Problem.objects.get_or_create(id=24, start='Lionel Messi', end='Angela Merkel')
	"""
