# Generated by Django 3.2.9 on 2021-11-27 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0016_alter_newsletter_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='frequency',
            field=models.IntegerField(choices=[(1, 'Daily'), (7, 'Weekly'), (30, 'Monthly')], default=7),
        ),
    ]
