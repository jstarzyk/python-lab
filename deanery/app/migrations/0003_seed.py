from random import choice

from django.contrib.auth.models import User, Group
from django.db import migrations

from app import models


def add_random_marks(subject, assignments, student):
    for _ in assignments:
        models.Mark.objects.create(
            subject=subject,
            assignments=assignments,
            student=student,
            value=choice(2.0, 3.0, 3.5, 4.0, 4.5, 5.0)
        )


def add_subject_with_assignments(name, n_assignments):
    subject = models.Subject.objects.create(name=name)
    assignments = []

    for i in range(n_assignments):
        assignments.append(models.Assignment.objects.create(
            name='lab' + str(i),
            subject=subject
        ))

    return subject, assignments


def add_person_with_user(username, password, first_name, last_name, group, subjects):
    user = User.objects.create_user(
        username=username,
        password=password,
        first_name=first_name,
        last_name=last_name,
    )

    user.groups.add(group)
    person = models.Student.objects.create(
        user=user,
        subjects=subjects
    )

    return person


def seed(apps, schema_editor):
    subjects_with_assignments = (
        add_subject_with_assignments('Python', 4),
        add_subject_with_assignments('Java', 6),
        add_subject_with_assignments('Erlang', 5)
    )

    subjects, assignments = zip(*subjects_with_assignments)

    admin_user = Group.objects.get(name='admin_user')
    standard_user = Group.objects.get(name='standard_user')

    students = (
        add_person_with_user('jkowalski', 'abcjk', 'Jan', 'Kowalski', standard_user, subjects),
        add_person_with_user('amalinowski', 'abcam', 'Adam', 'Malinowski', standard_user, subjects),
        add_person_with_user('jstarzyk', 'abcjs', 'Jakub', 'Starzyk', standard_user, subjects)
    )

    add_person_with_user('zkaleta', 'abczk', 'Zbigniew', 'Kaleta', admin_user, subjects)

    for pair in subjects_with_assignments:
        for student in students:
            add_random_marks(pair[0], pair[1], student)


class Migration(migrations.Migration):
    dependencies = [
        ('app', '0001_initial'),
        ('app', '0002_make_groups'),
    ]

    operations = [
        migrations.RunPython(seed),
    ]