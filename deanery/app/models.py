from django.db import models
from django.contrib.auth.models import User, Group, Permission


MARKS_VALUES = (20, 30, 35, 40, 45, 50)
MARKS_DISPLAY = ('2.0', '3.0', '3.5', '4.0', '4.5', '5.0')


class Subject(models.Model):
    name = models.CharField(
        unique=True,
        max_length=30
    )


class Person(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    subjects = models.ManyToManyField(Subject)

    class Meta:
        abstract = True


class Student(Person):
    pass


class Teacher(Person):
    pass


class Assignment(models.Model):
    name = models.CharField(
        max_length=30,
        null=True,
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.DO_NOTHING
    )


class Mark(models.Model):
    subject = models.ForeignKey(
        Subject,
        on_delete=models.DO_NOTHING
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.DO_NOTHING
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.DO_NOTHING
    )
    value = models.PositiveSmallIntegerField(
        choices=tuple(zip(MARKS_VALUES, MARKS_DISPLAY)),
        null=True
    )
