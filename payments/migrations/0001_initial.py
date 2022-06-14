# Generated by Django 3.2 on 2022-06-13 20:00

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import localflavor.br.models
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('transaction_amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Valor da Transação')),
                ('installments', models.IntegerField(verbose_name='Parcelas')),
                ('payment_method_id', models.CharField(max_length=250, verbose_name='Método de Pagamento')),
                ('email', models.EmailField(max_length=254)),
                ('doc_number', localflavor.br.models.BRCPFField(max_length=14, verbose_name='CPF')),
                ('mercado_pago_id', models.CharField(blank=True, db_index=True, max_length=250)),
                ('mercado_pago_status', models.CharField(blank=True, max_length=250)),
                ('mercado_pago_status_detail', models.CharField(blank=True, max_length=250)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='orders.order')),
            ],
            options={
                'ordering': ('-modified',),
            },
        ),
    ]
