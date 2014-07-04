from django.db import models


class Problem(models.Model):

    created_at = models.DateTimeField(auto_now=True)
    start = models.CharField(max_length=254)
    end = models.CharField(max_length=254)


class Result(models.Model):
    time = models.DateTimeField(auto_now=True)
    problem = models.ForeignKey('Problem')
    path_length = models.IntegerField()


def create_problems():
    """
    Function to populate the db
    """
    # easy
    Problem.objects.get_or_create(id=1, start='Jogi Löw', end='Angela Merkel')
    Problem.objects.get_or_create(id=2, start='John Lennon', end='Michael Jackson')
    Problem.objects.get_or_create(id=3, start='Jean-Claude van Damme', end='Arnold Schwarzenegger')
    
    #normal
    Problem.objects.get_or_create(id=4, start='Albert Einstein', end='Michael Jackson')
    Problem.objects.get_or_create(id=5, start='Kevin Großkreutz', end='Angela Merkel')
    Problem.objects.get_or_create(id=6, start='Angela Merkel', end='Kevin Großkreutz')
    Problem.objects.get_or_create(id=7, start='Johann Wolfgang von Goethe', end='Arnold Schwarzenegger')
    Problem.objects.get_or_create(id=8, start='August der Starke', end='Barack Obama')
   
    # hard
    Problem.objects.get_or_create(id=9, start='Erich Kästner', end='Otto Dix')
    Problem.objects.get_or_create(id=10, start='Donald Duck', end='Albert Camus')
