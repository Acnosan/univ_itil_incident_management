from django.db import migrations


CATEGORY_CHOICES = (
    ('hardware', 'Hardware'),
    ('software', 'Software'),
    ('network', 'Network'),
    ('printer', 'Printer'),
    ('phone', 'Phone'),
    ('laptop', 'Laptop'),
)
PRIORITY_CHOICES = (
    ('veryhigh', 'Very High'),
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
)
STATUS_CHOICES = (
    #('new', 'New'),
    ('pending', 'Pending'),
    ('ongoing', 'Ongoing'),
    ('solved', 'Solved'),
    ('closed', 'Closed'),
)

class Migration(migrations.Migration):

    def populate_categories(apps, schema_editor):
        CategoryModel = apps.get_model('app_l3', 'CategoryModel')
        for name, desc in CATEGORY_CHOICES:
            CategoryModel.objects.create(category_name=name, description=desc)

    def populate_priorities(apps, schema_editor):
        PriorityModel = apps.get_model('app_l3', 'PriorityModel')
        for name, desc in PRIORITY_CHOICES:
            PriorityModel.objects.create(priority_name=name, description=desc)

    def populate_status(apps, schema_editor):
        StatusModel = apps.get_model('app_l3', 'StatusModel')
        for name, desc in STATUS_CHOICES:
            StatusModel.objects.create(status_name=name, description=desc)

    dependencies = [
        ('app_l3', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(populate_categories),
        migrations.RunPython(populate_priorities),
        migrations.RunPython(populate_status),
    ]