# Generated by Django 3.2.9 on 2021-11-04 11:45

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20211104_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='climbingroutes',
            name='added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
