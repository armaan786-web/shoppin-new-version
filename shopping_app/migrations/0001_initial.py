# Generated by Django 4.1.5 on 2023-01-21 18:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_Date', models.DateField(auto_now_add=True)),
                ('daily_wise_commission', models.IntegerField(blank=True, default=0, null=True)),
                ('abc', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prodcut',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('duration', models.IntegerField()),
                ('commission', models.IntegerField()),
                ('product_img', models.ImageField(upload_to='product_img')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=100)),
                ('referral_id', models.CharField(blank=True, max_length=12)),
                ('refer_by', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField(auto_now_add=True)),
                ('wallet_request', models.CharField(choices=[('Pending', 'Pending'), ('Accept', 'Accept'), ('Reject', 'Reject')], default='Pending', max_length=50)),
                ('user', models.ManyToManyField(related_name='wallet_set', to='shopping_app.booking')),
            ],
        ),
        migrations.CreateModel(
            name='Recharge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upi_id', models.CharField(max_length=100)),
                ('amount', models.PositiveIntegerField()),
                ('utr', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
                ('recharge_request', models.CharField(choices=[('Pending', 'Pending'), ('Accept', 'Accept'), ('Reject', 'Reject')], default='Pending', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='Kyc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bank_holder_name', models.CharField(max_length=50)),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=100)),
                ('ifsc_code', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.profile')),
            ],
        ),
        migrations.CreateModel(
            name='commision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commision', models.IntegerField()),
                ('booking', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.booking')),
            ],
        ),
        migrations.AddField(
            model_name='booking',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.prodcut'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping_app.profile'),
        ),
    ]