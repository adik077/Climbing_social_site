# Generated by Django 3.2.9 on 2021-11-30 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_climbingroutes_official_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='climbingroutes',
            name='official_grade',
            field=models.ForeignKey(default='none', on_delete=models.SET('none'), to='routes.routegrade'),
        ),
    ]