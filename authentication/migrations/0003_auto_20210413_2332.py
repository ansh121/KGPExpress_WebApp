# Generated by Django 3.1.6 on 2021-04-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_customuser_notification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='verification_status',
            field=models.BooleanField(default=True),
        ),
    ]
