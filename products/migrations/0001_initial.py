# Generated by Django 4.2.4 on 2025-02-23 03:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=120, verbose_name='Category')),
                ('name_en', models.CharField(db_index=True, max_length=120, null=True, verbose_name='Category')),
                ('name_ar', models.CharField(db_index=True, max_length=120, null=True, verbose_name='Category')),
                ('image_link', models.ImageField(blank=True, null=True, upload_to='categories/%Y/%m/%d', verbose_name='Image')),
                ('slug', models.SlugField(max_length=120, unique=True, verbose_name='URL')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='products.category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255, null=True)),
                ('name_ar', models.CharField(max_length=255, null=True)),
                ('slug', models.SlugField(max_length=250, verbose_name='URL')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('description_en', models.TextField(null=True)),
                ('description_ar', models.TextField(null=True)),
                ('brand', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount_price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('images', models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d', verbose_name='Image')),
                ('image_2', models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d', verbose_name='Image2')),
                ('image_3', models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d', verbose_name='Image3')),
                ('image_4', models.ImageField(blank=True, null=True, upload_to='product_images/%Y/%m/%d', verbose_name='Image4')),
                ('in_stock', models.BooleanField(default=True)),
                ('is_top_seller', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.CreateModel(
            name='ProductType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_ar', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCharacteristic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('name_en', models.CharField(max_length=100, null=True)),
                ('name_ar', models.CharField(max_length=100, null=True)),
                ('value', models.CharField(max_length=255)),
                ('value_en', models.CharField(max_length=255, null=True)),
                ('value_ar', models.CharField(max_length=255, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='characteristics', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.producttype'),
        ),
    ]
