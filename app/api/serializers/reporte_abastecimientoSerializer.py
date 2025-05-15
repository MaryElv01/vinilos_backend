from datetime import date
from rest_framework import serializers
from app.models import *
from . import *

class ItemPedidoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer()
    
    class Meta:
        model = ItemPedido
        fields = ['producto', 'cantidad']



class Reporte_AbastecimientoSerializer(serializers.ModelSerializer):
    items = ItemPedidoSerializer(many=True)
    
    class Meta:
        model = Reporte_Abastecimiento
        fields = '__all__'
        read_only_fields = ['id', 'costoTot']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        reporte = Reporte_Abastecimiento.objects.create(**validated_data)
        total = 0

        for item_data in items_data:
            producto_data = item_data.pop('producto')
            cantidad = item_data['cantidad']
            
            # Crear N productos idénticos
            for _ in range(cantidad):
                producto = Producto.objects.create(
                    **producto_data,
                    disponible=False
                )
                ItemPedido.objects.create(
                    pedido=reporte,
                    producto=producto,
                    cantidad=1
                )
                total += producto.costo

        reporte.costoTot = total
        reporte.save()
        return reporte