from rest_framework import serializers
from ...models import Piercing

class PiercingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Piercing
        fields = '__all__'

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not value[0].isupper():
            raise serializers.ValidationError("El nombre debe comenzar con una letra mayúscula.")
        return value

