# Generated by Django 3.2.6 on 2021-10-12 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0010_auto_20211011_2146'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaluareform',
            name='telephone1',
        ),
        migrations.RemoveField(
            model_name='evaluareform',
            name='telephone2',
        ),
        migrations.AddField(
            model_name='presentationdata',
            name='strada',
            field=models.CharField(blank=True, choices=[('one_lane', 'O banda de circulatie'), ('two_lane', 'Doua benzi de circulatie'), ('three_lane', 'Trei benzi de circulatie')], max_length=155, null=True),
        ),
        migrations.AddField(
            model_name='presentationdata',
            name='zona',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='MarketAnalysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dps', models.TextField(blank=True, max_length=1000, null=True)),
                ('area_between', models.CharField(blank=True, max_length=155, null=True)),
                ('ac', models.TextField(blank=True, null=True)),
                ('zona_type', models.CharField(blank=True, choices=[('medii', 'medii'), ('sub medie', 'Sub medie'), ('above average', 'De vârstă medie/medii sau peste medie'), ('medium age', 'De varsta medie')], max_length=155, null=True)),
                ('af', models.TextField(blank=True, null=True)),
                ('const_density', models.CharField(blank=True, choices=[('mare', 'Mare'), ('medie', 'Medie')], max_length=55, null=True)),
                ('ebby', models.CharField(blank=True, max_length=155, null=True)),
                ('prop_size', models.CharField(blank=True, choices=[('medie', 'Medie'), ('mare', 'Mare'), ('mica', 'Mica')], max_length=155, null=True)),
                ('exposure', models.CharField(blank=True, choices=[('3', '3-9 luni'), ('6', '6-12 luni'), ('12', 'peste 12 luni')], max_length=155, null=True)),
                ('spi', models.TextField(blank=True, null=True)),
                ('liquidity', models.CharField(blank=True, choices=[('buna', 'Buna'), ('medie', 'Medie'), ('slaba', 'Slaba')], max_length=155, null=True)),
                ('transactions_nr', models.CharField(blank=True, choices=[('mediu', 'Mediu'), ('mare', 'Mare'), ('redus', 'Redus')], max_length=155, null=True)),
                ('exposure_period', models.CharField(blank=True, choices=[('scurte', 'Scurte'), ('lungi', 'Lungi')], max_length=155, null=True)),
                ('forecast', models.TextField(blank=True, null=True)),
                ('minsale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('maxsale_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('guarantee_risk', models.TextField(blank=True, null=True)),
                ('ref_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.evaluareform')),
            ],
        ),
    ]
