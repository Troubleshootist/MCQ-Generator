# Generated by Django 4.0.4 on 2022-05-12 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_gen', '0003_alter_questionsequence_sequence_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionresult',
            name='test_field',
        ),
    ]