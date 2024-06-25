# Generated by Django 5.0.6 on 2024-06-25 17:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('everywhere', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('scientific_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='account',
        ),
        migrations.CreateModel(
            name='Account_User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountuser_account', to='everywhere.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountuser_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('about', models.TextField()),
                ('joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PlantedTree',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField()),
                ('planted_at', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='plantedtree_account', to='everywhere.account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='plantedtree_user', to=settings.AUTH_USER_MODEL)),
                ('tree', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='plantedtree_tree', to='everywhere.tree')),
            ],
        ),
    ]
