# Generated by Django 3.2.6 on 2021-11-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0020_suprafete_is_utila'),
    ]

    operations = [
        migrations.AddField(
            model_name='valuatedproperty',
            name='assigned_to',
            field=models.CharField(blank=True, max_length=55, null=True),
        ),
    ]