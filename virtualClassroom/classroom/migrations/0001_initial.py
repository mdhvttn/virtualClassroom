# Generated by Django 3.2.7 on 2021-09-07 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authService', '0002_rename_username_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=50)),
                ('published_at', models.DateTimeField()),
                ('deadline', models.DateTimeField()),
                ('status', models.CharField(max_length=15)),
                ('assigned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_by', to='authService.profile')),
                ('assigned_to', models.ManyToManyField(related_name='profile_to', to='authService.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('assignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignment', to='classroom.assignments')),
                ('submitted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submittedby', to='authService.profile')),
            ],
        ),
    ]
