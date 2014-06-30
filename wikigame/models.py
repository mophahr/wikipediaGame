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
