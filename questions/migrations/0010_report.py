# Generated by Django 3.1.7 on 2021-03-22 02:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0009_auto_20210322_0158'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='questions.question')),
            ],
        ),
    ]