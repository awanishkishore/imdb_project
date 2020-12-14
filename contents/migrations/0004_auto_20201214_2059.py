# Generated by Django 3.1.4 on 2020-12-14 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contents', '0003_content_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='content_type',
            field=models.CharField(choices=[('movie', 'MOVIE'), ('tv show', 'TV SHOW'), ('documentary', 'DOCUMENTARY')], max_length=50, null=True),
        ),
    ]