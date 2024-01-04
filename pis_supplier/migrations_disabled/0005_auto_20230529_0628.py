# Generated by Django 3.0.7 on 2023-05-29 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pis_supplier', '0004_auto_20230529_0511'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierstatement',
            name='payment_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True),
        ),
        migrations.AlterField(
            model_name='supplierstatement',
            name='supplier_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=30, null=True),
        ),
    ]
