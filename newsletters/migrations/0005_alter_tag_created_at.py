# Generated by Django 3.2.9 on 2021-11-25 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0004_alter_tag_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
