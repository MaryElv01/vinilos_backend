from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from urllib.parse import urlparse
import os
import cloudinary.uploader
from rest_framework.decorators import action
from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrTatuador
from rest_framework.permissions import AllowAny
from ...models import Tattoo
from ..serializers import TattooSerializer

class TattooViewSet(viewsets.ModelViewSet):
    queryset = Tattoo.objects.all()
    serializer_class = TattooSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsSuperuserOrTatuador]
    authentication_classes = [CsrfExemptSessionAuthentication]

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='publicos')
    def publicos(self, request):
        """
        GET /api/tattoo/publicos/
        Devuelve solo los tattoos con public=True
        """
        qs = Tattoo.objects.filter(public=True)
        data = TattooSerializer(qs, many=True).data
        return Response(data)

    def perform_cloudinary_upload(self, file):
        result = cloudinary.uploader.upload(
            file,
            folder='vinilos/tattoo/'
        )
        return result.get('secure_url')

    def get_public_id_from_url(self, url):
        path = urlparse(url).path.lstrip('/')
        public_id, _ = os.path.splitext(path)
        return public_id

    def create(self, request, *args, **kwargs):
        image_file = request.FILES.get('foto')
        if image_file:
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tattoo = serializer.save()
            return Response(self.get_serializer(tattoo).data, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.foto:
            public_id = self.get_public_id_from_url(instance.foto.url)
            cloudinary.uploader.destroy(public_id)
        instance.delete()
        return Response({"message": "Tattoo eliminado"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_url = instance.foto.url if instance.foto else None

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            tattoo = serializer.save()
            return Response(self.get_serializer(tattoo).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            tattoo = serializer.save()
            return Response(self.get_serializer(tattoo).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
