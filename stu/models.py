from django.db import models
from teach.models import *


class Parents(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)
    tel = models.CharField(max_length=32, null=False)
    access_time = models.DateTimeField()
    status = models.CharField(max_length=256)


class Students(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)
    parent = models.ForeignKey(Parents)


class Seasons(NoDeleteModel):
    name = models.CharField(max_length=32, null=False)


class Grades(NoDeleteModel):
    season = models.ForeignKey(Seasons)
    subject = models.ForeignKey(Subjects)
    teacher = models.ForeignKey(Teachers)
    price = models.IntegerField(default=1, null=False)
    discount = models.FloatField(default=1.0, null=False)


class Scores(NoDeleteModel):
    grade = models.ForeignKey(Grades)
    student = models.ForeignKey(Students)
    test_time = models.DateTimeField(null=False)
    score = models.FloatField(default=0, null=False)


class Auditions(NoDeleteModel):
    teacher = models.ForeignKey(Teachers)
    student = models.ForeignKey(Students)
    success = models.BooleanField(default=False, null=False)


class Orders(NoDeleteModel):
    student = models.ForeignKey(Students)
    grade = models.ForeignKey(Grades)
    real_pay = models.FloatField(null=False)
    datetime = models.DateTimeField(null=False)

