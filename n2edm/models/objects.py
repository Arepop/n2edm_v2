from django.db import models

class Actor(models.Model):
    """Model of Actor for database storage
    """

class Action(models.Model):
    """Model of Action for database storaget
    """
    set = models.TextField(unique=True)
    name = models.TextField(unique=True)
    children = models.ForeignKey(Actor, on_delete=models.CASCADE)

class Group(models.Model):
    """Model of Group for database storage
    """
    set = models.TextField(unique=True)
    name = models.TextField(unique=True)
    children = models.ForeignKey(Action, on_delete=models.CASCADE)

class TimelineActor(models.Models):
    pass

class InfinityActor(models.Model):
    pass