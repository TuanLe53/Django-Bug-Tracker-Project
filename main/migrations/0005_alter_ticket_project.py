# Generated by Django 4.1.3 on 2023-04-03 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_alter_ticket_project"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="main.project"
            ),
        ),
    ]