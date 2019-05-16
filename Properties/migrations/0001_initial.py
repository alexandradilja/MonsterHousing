# Generated by Django 2.2.1 on 2019-05-15 19:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=255)),
                ('house_no', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=255)),
                ('zip', models.IntegerField()),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=255)),
                ('price', models.FloatField()),
                ('rooms', models.IntegerField()),
                ('description', models.CharField(max_length=999)),
                ('property_image', models.CharField(max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elevator', models.BooleanField()),
                ('garage', models.BooleanField()),
                ('near_bloodbank', models.BooleanField()),
                ('dungeon', models.BooleanField()),
                ('secret_entrance', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=999)),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField()),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Addresses')),
                ('detail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Details')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='details',
            name='tags',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Tags'),
        ),
        migrations.AddField(
            model_name='details',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Types'),
        ),
        migrations.AddField(
            model_name='addresses',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Properties.Cities'),
        ),
    ]
