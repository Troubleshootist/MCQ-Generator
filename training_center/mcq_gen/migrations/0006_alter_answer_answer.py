# Generated by Django 4.0.4 on 2022-04-29 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_gen', '0005_alter_question_changed_by_alter_question_checked_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(max_length=400),
        ),
    ]