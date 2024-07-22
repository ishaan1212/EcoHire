# Generated by Django 5.0.7 on 2024-07-21 23:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EnvironmentalInitiative',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=100)),
                ('organization', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='UserContribution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contribution_details', models.TextField()),
                ('contribution_date', models.DateField(auto_now_add=True)),
                ('initiative', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myApp.environmentalinitiative')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
