from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=30, null=False, unique=True)
    password = models.CharField(max_length=32, null=False)
    email = models.EmailField(max_length=50, null=False)

class Cases(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    desc = models.CharField(max_length=30, null=True)
    url = models.TextField(null=False)
    method = models.CharField(max_length=10, null=True)
    headers = models.TextField(null=True)
    body = models.TextField(null=True)
    checks = models.TextField(null=False)

class Task(models.Model):
    name = models.CharField(max_length=20, null=False, unique=True)
    description = models.CharField(max_length=50, null=True)
    cases = models.ManyToManyField(Cases)

class History(models.Model):
    time = models.FloatField(null=False, unique=True)
    status = models.IntegerField(choices=((0, 'running'), (1, 'finish')), null=True)
    report = models.CharField(max_length=100, null=True)
    task = models.ForeignKey(Task)

    def __unicode__(self):
        return self.id


