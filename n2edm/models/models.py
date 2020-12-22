from django.db import models



class Group(models.Model):
    """Model of Group for database storage
    """
    set_id = models.TextField()
    name = models.TextField()

class Action(models.Model):
    """Model of Action for database storaget
    """
    set_id = models.TextField()
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class Actor(models.Model):
    """Model of Actor for database storage
    """

class TimelineActor(models.Model):
    set_id = models.TextField()


class InfinityActor(models.Model):
    pass