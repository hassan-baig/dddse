# Generated by Django 2.2 on 2019-04-16 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cockpit', '0014_auto_20190415_1847'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wish',
            name='id',
        ),
        migrations.AlterField(
            model_name='wish',
            name='fid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
