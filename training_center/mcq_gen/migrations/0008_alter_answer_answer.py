# Generated by Django 4.0.4 on 2022-04-30 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcq_gen', '0007_alter_question_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='answer',
            field=models.CharField(default=False, max_length=400),
        ),
    ]
