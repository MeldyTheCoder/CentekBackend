# Generated by Django 5.0.3 on 2024-03-29 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('med', '0010_alter_user_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='image',
            new_name='avatar',
        ),
    ]
