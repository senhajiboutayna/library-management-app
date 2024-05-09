# Generated by Django 5.0.4 on 2024-05-09 22:04

import datetime
import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_title', models.CharField(max_length=200)),
                ('book_author', models.CharField(max_length=100)),
                ('book_pages', models.PositiveIntegerField()),
                ('summary', models.TextField(blank=True, help_text='Summary about the book', max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('roll_number', models.CharField(max_length=100, unique=True)),
                ('fullname', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=100)),
                ('program', models.CharField(max_length=100)),
                ('Email', models.EmailField(help_text='Student e-mail', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BookInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Book unique id across the Library', primary_key=True, serialize=False)),
                ('book_number', models.PositiveIntegerField(help_text='Book number for books of the save kind', null=True)),
                ('Is_borrowed', models.BooleanField(default=False)),
                ('book', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='biblio.book')),
            ],
        ),
        migrations.CreateModel(
            name='Book_Issue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateTimeField(auto_now=True, help_text='Date the book is issued')),
                ('due_date', models.DateTimeField(default=datetime.datetime(2024, 5, 18, 0, 4, 13, 538957), help_text='Date the book is due to')),
                ('date_returned', models.DateField(blank=True, help_text='Date the book is returned', null=True)),
                ('remarks_on_issue', models.CharField(default='Book in good condition', help_text='Book remarks/condition during issue', max_length=100)),
                ('remarks_on_return', models.CharField(default='Book in good condition', help_text='Book remarks/condition during return', max_length=100)),
                ('book_instance', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblio.bookinstance')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='biblio.students')),
            ],
        ),
    ]
