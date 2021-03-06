# Generated by Django 2.2.1 on 2019-05-17 03:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Properties', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssn', models.CharField(max_length=50, unique=True)),
                ('phone', models.CharField(max_length=50)),
                ('profile_image', models.CharField(max_length=999)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Addresses')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
