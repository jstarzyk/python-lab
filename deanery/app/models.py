from django.db import models
from django.contrib.auth.models import User, Group, Permission


# class User(models.Model):
#     username = models.CharField(unique=True)
#     password: models.CharField()
#     role = models.CharField(choices=('student', 'teacher'))

# class Student(Group):
#     name = 'student'
#
#
# class Teacher(Group):
#     name = 'teacher'


class Subject(models.Model):
    name = models.CharField(
        unique=True,
        max_length=30
    )
    # students = models.ManyToManyField(Student)


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
    value = models.DecimalField(
        choices=(
            (2.0, '2.0'),
            (3.0, '3.0'),
            (3.5, '3.5'),
            (4.0, '4.0'),
            (4.5, '4.5'),
            (5.0, '5.0')
        ),
        decimal_places=2,
        max_digits=2
    )
