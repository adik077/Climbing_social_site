# Generated by Django 3.2.9 on 2021-11-30 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0009_remove_climbingroutes_official_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climbingroutes',
            name='category',
            field=models.CharField(default='Mountains', max_length=100),
        ),
    ]
