from rest_framework import serializers
from app.api.permissions.permissions import IsSuperuserOrTatuador
from app.models import Reporte_Venta

class Reporte_VentaSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.CharField(write_only=True)
    productos = serializers.PrimaryKeyRelatedField(many=True, read_only=True) 
    permission_classes = [IsSuperuserOrTatuador]

    class Meta:
        model = Reporte_Venta
        fields = '__all__'
        read_only_fields = ['id', 'fecha', 'productos', 'aporte']