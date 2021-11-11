# Generated by Django 3.2.6 on 2021-11-10 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0006_auto_20211110_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='comparableproperty',
            name='opt1_name',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt1_val',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt2_name',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt2_val',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt3_name',
            field=models.CharField(blank=True, max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt3_val',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]