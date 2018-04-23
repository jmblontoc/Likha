# Generated by Django 2.0.4 on 2018-04-21 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('datacollection', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('Barangay Nutrition Scholar', 'Barangay Nutrition Scholar'), ('Nutritionist', 'Nutritionist'), ('Nutrition Program Coordinator', 'Nutrition Program Coordinator')], max_length=40)),
                ('barangay', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='datacollection.Barangay')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
