# Generated by Django 4.2.16 on 2024-09-04 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ingredients', models.CharField(help_text='Enter recipe ingredients, separated by a comma', max_length=225)),
                ('cooking_time', models.IntegerField(help_text='Enter cooking time in minutes.')),
            ],
        ),
    ]
