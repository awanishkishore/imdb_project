# Generated by Django 3.1.4 on 2020-12-13 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='name',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(db_index=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='rating',
            name='rating',
            field=models.PositiveIntegerField(db_index=True, null=True),
        ),
        migrations.AlterModelTable(
            name='comment',
            table='comment',
        ),
        migrations.AlterModelTable(
            name='content',
            table='content',
        ),
        migrations.AlterModelTable(
            name='genre',
            table='genre',
        ),
        migrations.AlterModelTable(
            name='rating',
            table='rating',
        ),
    ]
