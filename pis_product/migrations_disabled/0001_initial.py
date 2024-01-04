# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-27 07:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pis_retailer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('brand_name', models.CharField(max_length=200)),
                ('retailer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='retailer_product', to='pis_retailer.Retailer')),
            ],
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('retail_price', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('consumer_price', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('available_item', models.IntegerField(default=1)),
                ('purchased_item', models.IntegerField(default=0)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_detail', to='pis_product.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PurchasedProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('manual_discount', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('discount_percentage', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('purchase_amount', models.DecimalField(decimal_places=2, default=0, max_digits=65)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_product', to='pis_product.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
