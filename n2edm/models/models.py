from django.db import models


class Group(models.Model):
    """Model of Group for database storage"""

    set_id = models.TextField(default=0)
    name = models.TextField()
    position = models.IntegerField(null=True)
    # max_pos = models.IntegerField()


class Action(models.Model):
    """Model of Action for database storaget"""

    set_id = models.TextField(default=0)
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    start_cmd = models.TextField()
    stop_cmd = models.TextField(null=True)
    duration = models.IntegerField()
    params = models.TextField()
    color = models.TextField()
    position = models.IntegerField(null=True)


class Actor(models.Model):
    """Model of Actor for database storage"""

    set_id = models.TextField(default=0)
    name = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    action = models.ForeignKey(Action, on_delete=models.CASCADE)
    params = models.TextField()
    color = models.TextField()
    start = models.IntegerField()
    stop = models.IntegerField()
    annotate = models.TextField()
    text = models.TextField()


class TimelineActor(models.Model):
    set_id = models.TextField(default=0)


class InfinityActor(models.Model):
    set_id = models.TextField(default=0)
