from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from ...models import Reporte_Finanza


class Reporte_FinanzaSerializer(serializers.ModelSerializer):
    source_type = serializers.SerializerMethodField()
    source_id   = serializers.IntegerField(source='object_id')

    class Meta:
        model  = Reporte_Finanza
        fields = [
            'id', 'date', 'transaction_type', 'description',
            'amount', 'source_type', 'source_id'
        ]

    def get_source_type(self, obj):
        return obj.content_type.model_class().__name__
