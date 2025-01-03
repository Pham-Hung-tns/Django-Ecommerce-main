# Generated by Django 5.1.2 on 2024-11-16 15:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_alter_item_custom_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='add_information',
            field=models.TextField(default='Default information'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('D', 'Dress'), ('S', 'Shoes'), ('G', 'Gift')], max_length=2),
        ),
        migrations.CreateModel(
            name='AdditionImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='addition_images/')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addition_images', to='core.item')),
            ],
        ),
    ]
