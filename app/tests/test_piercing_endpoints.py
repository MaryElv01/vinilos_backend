from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from app.models import Piercing

class PublicPiercingEndpointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear piercings de prueba
        cls.public_piercing = Piercing.objects.create(
            nombre="Piercing Público",
            ubi="lobulo",
            precio=300,
            public=True
        )
        cls.private_piercing = Piercing.objects.create(
            nombre="Piercing Privado",
            ubi="helix",
            precio=400,
            public=False
        )
    
    def test_public_piercings_endpoint(self):
        """Test para el endpoint público de piercings"""
        url = reverse('piercing-publicos')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Solo debe devolver el piercing público
        self.assertEqual(response.data[0]['nombre'], "Piercing Público")
    
    def test_list_piercings_endpoint(self):
        """Test para el listado general de piercings"""
        url = reverse('piercing-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Devuelve todos los piercings