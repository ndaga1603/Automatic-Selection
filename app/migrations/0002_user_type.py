# Generated by Django 4.2.1 on 2023-06-28 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('necta', 'necta'), ('admin', 'admin')], default='admin', max_length=20),
        ),
    ]
