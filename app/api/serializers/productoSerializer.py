from datetime import date
from rest_framework import serializers
from ...models import Producto

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['nombre', 'cat', 'costo', 'precio', 'foto', 'fecha_v', 'disponible']
        
    def validate_nombre(self, value):
        value = value.lower().replace(' ', '_')
        if value not in [choice[0] for choice in Producto.NOMBRES]:
            raise serializers.ValidationError("Nombre no válido")
        return value

    def validate_cat(self, value):
        # Convierte "Materiales" → "materiales"
        value = value.lower()
        if value not in dict(Producto.CATEGORIA).keys():
            raise serializers.ValidationError(
                f"Categoría inválida. Valores permitidos: {[v[1] for v in Producto.CATEGORIA]}"
            )
        return value

class VenderProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'disponible', 'fecha_v']
        read_only_fields = ['id']
    
    def update(self, instance, validated_data):
        instance.disponible = False
        instance.fecha_v = date.today()
        instance.save()
        return instance