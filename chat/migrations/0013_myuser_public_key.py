# Generated by Django 5.1.1 on 2024-09-23 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_alter_message_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='public_key',
            field=models.TextField(blank=True, null=True),
        ),
    ]
