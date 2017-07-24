# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-11 06:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(max_length=20, null=True, unique=True)),
                ('user_type', models.CharField(choices=[('U', 'User'), ('C', 'Client'), ('A', 'Admin')], max_length=1, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('name', models.CharField(max_length=100)),
                ('branch_alias', models.CharField(blank=True, help_text='Field that will be used on the front-end when displaying the branch name.', max_length=100, null=True)),
                ('location', models.TextField()),
                ('phone', models.CharField(blank=True, default=None, max_length=20, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.Account')),
            ],
            options={
                'ordering': ('-create_at',),
            },
        ),
        migrations.CreateModel(
            name='BranchSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.DateTimeField(editable=False, null=True)),
                ('day', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=10)),
                ('start', models.TimeField()),
                ('end', models.TimeField()),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='user.Branch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='branch',
            unique_together=set([('name', 'account')]),
        ),
    ]
