from django.db import models


class Group(models.Model):
    """Model of Group for database storage"""

    set_id = models.TextField()
    name = models.TextField()
    position = models.IntegerField()


class Action(models.Model):
    """Model of Action for database storaget"""

    set_id = models.TextField()
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    start_cmd = models.TextField()
    stop_cmd = models.TextField()
    duration = models.IntegerField()
    params = models.TextField()
    color = models.TextField()


class Actor(models.Model):
    """Model of Actor for database storage"""

    set_id = models.TextField()
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    params = models.TextField()
    color = models.TextField()
    start = models.IntegerField()
    stop = models.IntegerField()
    annotate = models.TextField()
    text = models.TextField()


class TimelineActor(models.Model):
    set_id = models.TextField()


class InfinityActor(models.Model):
    pass