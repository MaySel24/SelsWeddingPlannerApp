# Generated by Django 5.1.7 on 2025-03-19 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planner', '0004_alter_guest_options_guest_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeddingColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hex_code', models.CharField(help_text='Enter a HEX code like #FFC0CB', max_length=7)),
            ],
        ),
    ]
