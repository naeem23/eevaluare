# Generated by Django 3.2.6 on 2021-10-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0016_auto_20211022_2129'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuatedproperty',
            name='construction_year',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
        migrations.AddField(
            model_name='valuatedproperty',
            name='height',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]