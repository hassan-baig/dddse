# Generated by Django 2.2 on 2019-04-16 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cockpit', '0015_auto_20190416_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='analyzedfeedbacks',
            name='id',
        ),
        migrations.RemoveField(
            model_name='democratic',
            name='id',
        ),
        migrations.AlterField(
            model_name='analyzedfeedbacks',
            name='fid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='democratic',
            name='fid',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
