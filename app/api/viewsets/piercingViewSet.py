from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from urllib.parse import urlparse
import os
import cloudinary.uploader
from rest_framework.decorators import action
from app.api.permissions.authentication import CsrfExemptSessionAuthentication
from app.api.permissions.permissions import IsSuperuserOrPerforador
from rest_framework.permissions import AllowAny
from ...models import Piercing
from ..serializers import PiercingSerializer

class PiercingViewSet(viewsets.ModelViewSet):
    queryset = Piercing.objects.all()
    serializer_class = PiercingSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsSuperuserOrPerforador]
    

    @action(detail=False, methods=['get'], permission_classes=[AllowAny], url_path='publicos')
    def publicos(self, request):
        """
        GET /api/piercing/publicos/
        Devuelve solo los piercings public=True
        """
        qs = Piercing.objects.filter(public=True)
        data = PiercingSerializer(qs, many=True).data
        return Response(data, status=status.HTTP_200_OK)

    def perform_cloudinary_upload(self, file):
        result = cloudinary.uploader.upload(
            file,
            folder='vinilos/piercings/'
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
            piercing = serializer.save()
            return Response(self.get_serializer(piercing).data, status=status.HTTP_201_CREATED)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.foto:
            public_id = self.get_public_id_from_url(instance.foto)
            cloudinary.uploader.destroy(public_id)
        instance.delete()
        return Response({"message": "Piercing eliminado"}, status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_url = instance.foto if instance.foto else None

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            piercing = serializer.save()
            return Response(self.get_serializer(piercing).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        old_url = instance.foto if instance.foto else None

        image_file = request.FILES.get('foto')
        if image_file:
            if old_url:
                public_id = self.get_public_id_from_url(old_url)
                cloudinary.uploader.destroy(public_id)
            url = self.perform_cloudinary_upload(image_file)
            request.data['foto'] = url

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            piercing = serializer.save()
            return Response(self.get_serializer(piercing).data, status=status.HTTP_200_OK)
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
