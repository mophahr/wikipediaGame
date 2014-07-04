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
    Problem.objects.get_or_create(id=1, start='Albert Einstein', end='Michael Jackson')
    Problem.objects.get_or_create(id=2, start='Angela Merkel', end='Kevin Großkreutz')
    Problem.objects.get_or_create(id=3, start='Kevin Großkreutz', end='Angela Merkel')
    Problem.objects.get_or_create(id=4, start='Erich Kästner', end='Otto Dix')
    Problem.objects.get_or_create(id=5, start='Johann Wolfgang von Goethe', end='Arnold Schwarzenegger')
    Problem.objects.get_or_create(id=7, start='Donald Duck', end='Albert Camus')
