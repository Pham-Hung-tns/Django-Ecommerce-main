# Generated by Django 5.1.2 on 2024-11-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_item_add_information_alter_item_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('Dr', 'Dress'), ('Sh', 'Shoes'), ('Gi', 'Gift')], max_length=2),
        ),
    ]
