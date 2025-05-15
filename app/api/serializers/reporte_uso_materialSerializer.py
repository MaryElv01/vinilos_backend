from rest_framework import serializers
from app.api.permissions.permissions import IsSuperuserOrTatuador
from app.models.reporte_uso_material import Reporte_Uso_Material

class Reporte_Uso_MaterialSerializer(serializers.ModelSerializer):
    material_nombre = serializers.CharField(write_only=True)
    materiales = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = Reporte_Uso_Material
        fields = ['id', 'fecha', 'materiales', 'cantidad', 'material_nombre']
        read_only_fields = ['id', 'fecha', 'materiales']