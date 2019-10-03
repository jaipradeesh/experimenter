# Generated by Django 2.1.11 on 2019-10-03 21:53

from difflib import SequenceMatcher as SM

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def closest_user(users, target_name):
    return sorted(
        [(SM(None, user.email, target_name).ratio(), user) for user in users],
        reverse=True,
    )[0][1]


def forward_analysis_owner(apps, schema_editor):
    Experiment = apps.get_model("experiments", "Experiment")
    User = apps.get_model(*settings.AUTH_USER_MODEL.split("."))

    for experiment in Experiment.objects.all():
        experiment.new_analysis_owner = closest_user(
            User.objects.all(), experiment.analysis_owner
        )
        experiment.save()


def reverse_analysis_owner(apps, schema_editor):
    Experiment = apps.get_model("experiments", "Experiment")

    for experiment in Experiment.objects.all():
        experiment.analysis_owner = experiment.new_analysis_owner.email
        experiment.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("experiments", "0072_changelog_pruning"),
    ]

    operations = [
        migrations.AddField(
            model_name="experiment",
            name="new_analysis_owner",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="analyzed_experiments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(forward_analysis_owner, reverse_analysis_owner),
        migrations.RemoveField(model_name="experiment", name="analysis_owner"),
        migrations.RenameField(
            model_name="experiment",
            old_name="new_analysis_owner",
            new_name="analysis_owner",
        ),
    ]
