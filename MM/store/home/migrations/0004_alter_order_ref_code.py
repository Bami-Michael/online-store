# Generated by Django 4.2.10 on 2024-04-25 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_order_ref_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.IntegerField(default=1419),
        ),
    ]
