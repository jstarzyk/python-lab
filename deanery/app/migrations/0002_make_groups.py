from django.contrib.auth.models import Group
from django.db import migrations


def add_groups(apps, schema_editor):
    Group.objects.get_or_create(name='admin_user')
    Group.objects.get_or_create(name='standard_user')


class Migration(migrations.Migration):
    # initial = False

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]