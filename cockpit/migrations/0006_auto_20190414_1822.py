# Generated by Django 2.2 on 2019-04-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cockpit', '0005_remove_feedbacks_fid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='democratic',
            name='nvotes',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='democratic',
            name='pvotes',
            field=models.IntegerField(blank=True),
        ),
    ]
