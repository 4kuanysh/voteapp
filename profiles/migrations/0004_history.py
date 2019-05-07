# Generated by Django 2.1.5 on 2019-05-07 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profiles', '0003_auto_20190501_1646'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coefficient_who_vote', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mark_who_vote', models.IntegerField()),
                ('value_for_whom_vote', models.DecimalField(decimal_places=2, max_digits=5)),
                ('date_voting', models.DateTimeField(auto_now_add=True)),
                ('for_whom_vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes_for_him', to=settings.AUTH_USER_MODEL)),
                ('who_vote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='his_votes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
