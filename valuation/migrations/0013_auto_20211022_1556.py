# Generated by Django 3.2.6 on 2021-10-22 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0012_alter_construction_floors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='construction',
            name='additional_equipment',
        ),
        migrations.RemoveField(
            model_name='construction',
            name='build_in',
        ),
        migrations.RemoveField(
            model_name='construction',
            name='etaj',
        ),
        migrations.RemoveField(
            model_name='construction',
            name='heating',
        ),
        migrations.AddField(
            model_name='construction',
            name='conform_text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='construction',
            name='dotari',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='construction',
            name='ef_choice',
            field=models.CharField(blank=True, choices=[('medii', 'Medii'), ('bune', 'Bune')], max_length=55, null=True),
        ),
        migrations.AddField(
            model_name='construction',
            name='pardoseli',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='construction',
            name='exterior_carpentry',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='construction',
            name='exterior_finishes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='construction',
            name='floors',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='valuation.floortype'),
        ),
        migrations.AlterField(
            model_name='construction',
            name='walls',
            field=models.TextField(blank=True, null=True),
        ),
    ]