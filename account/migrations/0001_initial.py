# Generated by Django 3.2.8 on 2021-10-23 13:33

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
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(default='0000FF', max_length=6)),
                ('birthday', models.DateField()),
                ('description', models.TextField()),
                ('avatar', models.ImageField(upload_to='')),
                ('pronouns', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Alter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('avatar', models.ImageField(upload_to='')),
                ('pronouns', models.CharField(max_length=32)),
                ('color', models.CharField(default='0000FF', max_length=6)),
                ('birthday', models.DateField()),
                ('description', models.TextField()),
                ('roles', models.CharField(max_length=32)),
                ('is_fragment', models.BooleanField()),
                ('groups', models.CharField(max_length=512)),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relation', models.CharField(choices=[('FR', 'Friend'), ('BL', 'Blocked'), ('RE', 'Requesting'), ('CH', 'Just Chatting')], default='CH', max_length=2)),
                ('left_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='left_user', to='account.account')),
                ('right_user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='right_user', to='account.account')),
            ],
        ),
        migrations.CreateModel(
            name='Front',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_main', models.BooleanField()),
                ('age', models.IntegerField()),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField(null=True)),
                ('front_type', models.CharField(choices=[('FR', 'Fronting'), ('CO', 'Co-Conscious'), ('BL', 'Blent')], max_length=2)),
                ('alter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.alter')),
                ('system', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.system')),
            ],
        ),
        migrations.AddField(
            model_name='alter',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.system'),
        ),
        migrations.AddField(
            model_name='account',
            name='system',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.system'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
