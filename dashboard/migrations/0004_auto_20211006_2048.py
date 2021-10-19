# Generated by Django 3.2.6 on 2021-10-06 14:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_comparableproperty_correct_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comparabletable',
            name='ape_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='balcon_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='comparables',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='cp_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='cy_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='etaj_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='fc_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='finish_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='hs_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='lc_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='me_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='parking_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='property_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='sc_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='su_motivation',
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='ape_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='balcon_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='cp_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='cy_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='etaj_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='fc_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='finish_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='hs_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='lc_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='me_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='parking_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='property_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='sc_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='su_motivation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='comparabletable',
            name='comparable',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.comparableproperty'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='ape_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='ape_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='balcon_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='balcon_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='cp_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='cp_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='cy_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='cy_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='etaj_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='etaj_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='fc_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='fc_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='finish_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='finish_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='hs_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='hs_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='lc_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='lc_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='margin',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='me_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='me_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='mobila_ajustare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='parking_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='parking_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='pb_ajustare',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='price_persqm',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='property_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='property_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='sc_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='sc_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='su_euro',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='comparabletable',
            name='su_percent',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
