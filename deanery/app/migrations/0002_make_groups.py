from django.conf import settings
from django.db import models, migrations
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType


# def add_permissions():
#     Permission.objects.get_or_create(
#         codename='any',
#         name='Access all data'
#     )
#     Permission.objects.get_or_create(
#         codename='self',
#         name='Access own data'
#     )


def add_groups(apps, schema_editor):
    Group.objects.get_or_create(name='admin_user')
    Group.objects.get_or_create(name='standard_user')


class Migration(migrations.Migration):
    initial = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(add_groups),
    ]