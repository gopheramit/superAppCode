# Generated by Django 4.0.7 on 2022-09-06 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_basics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomersDataNew',
            fields=[
                ('id', models.TextField(default=None, primary_key=True, serialize=False)),
                ('ewallet', models.TextField()),
                ('name', models.TextField()),
                ('email', models.TextField()),
                ('phone_number', models.TextField()),
            ],
        ),
    ]