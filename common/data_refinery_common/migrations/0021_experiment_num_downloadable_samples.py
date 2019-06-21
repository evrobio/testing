# Generated by Django 2.1.8 on 2019-06-12 17:25

import django.contrib.postgres.fields
from django.db import migrations, models

def update_cached_values(apps, schema_editor):
    """ """
    Experiment = apps.get_model('data_refinery_common', 'Experiment')
    ComputationalResultAnnotation = apps.get_model('data_refinery_common', 'ComputationalResultAnnotation')
    for experiment in Experiment.objects.all():
        organism_ids = list(ComputationalResultAnnotation.objects.filter(data__is_qn=True).values_list('data__organism_id', flat=True))
        experiment.num_downloadable_samples = experiment.samples.filter(is_processed=True, organism__id__in=organism_ids).count()
        experiment.save()

class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0020_update_qn_bucket'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='num_downloadable_samples',
            field=models.IntegerField(default=0),
        ),
        migrations.RunPython(update_cached_values)        
    ]