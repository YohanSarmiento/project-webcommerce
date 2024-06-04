# Generated by Django 5.0.4 on 2024-06-01 20:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_historialcambioproducto_fecha_cambio_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productocambio',
            old_name='descripcion',
            new_name='descripcion_anterior',
        ),
        migrations.RenameField(
            model_name='productocambio',
            old_name='imagen',
            new_name='imagen_anterior',
        ),
        migrations.RenameField(
            model_name='productocambio',
            old_name='nombre',
            new_name='nombre_anterior',
        ),
        migrations.RenameField(
            model_name='productocambio',
            old_name='precio',
            new_name='precio_anterior',
        ),
        migrations.RenameField(
            model_name='productocambio',
            old_name='stock',
            new_name='stock_anterior',
        ),
        migrations.RemoveField(
            model_name='productocambio',
            name='categorias',
        ),
        migrations.RemoveField(
            model_name='productocambio',
            name='proveedor',
        ),
        migrations.AddField(
            model_name='productocambio',
            name='categorias_anterior',
            field=models.ManyToManyField(blank=True, related_name='categorias_anterior', to='store.categoria'),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='categorias_nuevo',
            field=models.ManyToManyField(blank=True, related_name='categorias_nuevo', to='store.categoria'),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='descripcion_nueva',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='imagen_nueva',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='nombre_nuevo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='precio_nuevo',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='proveedor_anterior',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proveedor_anterior', to='store.proveedor'),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='proveedor_nuevo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='proveedor_nuevo', to='store.proveedor'),
        ),
        migrations.AddField(
            model_name='productocambio',
            name='stock_nuevo',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]