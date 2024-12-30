from django.db import migrations, models
import uuid

def generate_unique_custom_id(apps, schema_editor):
    Item = apps.get_model('core', 'Item')
    for item in Item.objects.all():
        item.custom_id = str(uuid.uuid4())
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_userprofile_stripe_customer_id'),  # Thay đổi tên file migration trước đó
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='custom_id',
            field=models.CharField(max_length=255, unique=True, blank=True, null=True),
        ),
        migrations.RunPython(generate_unique_custom_id),
    ]

