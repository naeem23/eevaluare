# Generated by Django 3.2.6 on 2021-10-21 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0011_auto_20211021_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='construction',
            name='floors',
            field=models.TextField(blank=True, null=True),
        ),
    ]
