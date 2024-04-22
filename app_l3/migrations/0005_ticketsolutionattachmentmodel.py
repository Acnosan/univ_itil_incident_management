# Generated by Django 5.0.2 on 2024-04-22 20:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_l3', '0004_ticketsmodel_attachment'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketSolutionAttachmentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='downloaded_solutions/')),
                ('targeted_solution', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app_l3.ticketsolutionmodel')),
            ],
            options={
                'db_table': 'tickets_solutions_attachment_table',
            },
        ),
    ]
