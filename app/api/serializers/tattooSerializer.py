from rest_framework import serializers
from ...models import Tattoo

class TattooSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tattoo
        fields = '__all__'

    def validate_nombre(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("El nombre debe tener al menos 3 caracteres.")
        if not value[0].isupper():
            raise serializers.ValidationError("El nombre debe comenzar con una letra mayúscula.")
        return value

    def validate_precio(self, value):
        if value <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que 0.")
        return value

    def validate_estilo(self, value):
        estilos_validos = [choice[1] for choice in Tattoo.ESTILOS]
        if value.lower() not in estilos_validos:
            raise serializers.ValidationError("El estilo debe ser uno de los valores permitidos.")
        return value

    def validate_artista(self, value):
        artistas_validos = [choice[1] for choice in Tattoo.ARTISTS]
        if value.lower() not in artistas_validos:
            raise serializers.ValidationError("El artista debe ser uno de los valores permitidos.")
        return value
