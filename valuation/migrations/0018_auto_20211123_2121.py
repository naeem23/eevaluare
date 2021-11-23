# Generated by Django 3.2.6 on 2021-11-23 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0017_remove_marketanalysis_range'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparableproperty',
            name='lat',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='lng',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='valuatedproperty',
            name='latitude',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='valuatedproperty',
            name='longitude',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
