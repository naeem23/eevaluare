# Generated by Django 3.2.6 on 2021-11-10 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('valuation', '0007_auto_20211110_1534'),
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
            name='opt1_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='opt1_name',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='opt2_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='opt2_name',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='opt3_motivation',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='opt3_name',
        ),
        migrations.RemoveField(
            model_name='comparabletable',
            name='pr_motivation',
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
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='balcon_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='cp_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='cy_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='etaj_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='fc_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='finish_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='hs_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='lc_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='me_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt1_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt2_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='opt3_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='pr_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='sc_motivation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='comparableproperty',
            name='su_motivation',
            field=models.TextField(blank=True, null=True),
        ),
    ]