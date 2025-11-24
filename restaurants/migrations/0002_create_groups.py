from django.db import migrations
from django.contrib.auth.models import Group

def create_groups(apps, schema_editor):
    Group.objects.get_or_create(name="users")
    Group.objects.get_or_create(name="restaurant_owners")

def delete_groups(apps, schema_editor):
    Group.objects.filter(name="users").delete()
    Group.objects.filter(name="restaurant_owners").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0001_initial'),  # <-- проверь, чтобы это была последняя твоя миграция
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]
