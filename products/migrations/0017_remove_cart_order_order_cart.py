# Generated by Django 4.0.5 on 2022-09-16 19:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_alter_cart_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='products.cart'),
        ),
    ]
