# Generated by Django 3.2.6 on 2021-10-19 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0002_auto_20211019_1805'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Utility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='construction',
            name='additional_equipment',
        ),
        migrations.RemoveField(
            model_name='construction',
            name='utilities',
        ),
        migrations.AddField(
            model_name='construction',
            name='additional_equipment',
            field=models.ManyToManyField(blank=True, to='valuation.AdditionalEquipment'),
        ),
        migrations.AddField(
            model_name='construction',
            name='utilities',
            field=models.ManyToManyField(blank=True, to='valuation.Utility'),
        ),
    ]