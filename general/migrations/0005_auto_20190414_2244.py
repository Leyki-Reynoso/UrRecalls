# Generated by Django 2.2 on 2019-04-14 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0004_auto_20190413_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recallsdrugs',
            old_name='Consequence',
            new_name='RecallDistribution',
        ),
    ]
