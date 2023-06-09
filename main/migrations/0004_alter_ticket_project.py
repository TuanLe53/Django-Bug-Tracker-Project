# Generated by Django 4.1.3 on 2023-04-03 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_project_team"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="project",
                to="main.project",
            ),
        ),
    ]
