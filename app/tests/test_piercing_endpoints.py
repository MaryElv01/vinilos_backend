from django.urls import reverse
from rest_framework.test import APITestCase
from app.models import Piercing
from rest_framework import status

class PiercingEndpointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Datos iniciales para las pruebas
        cls.piercing = Piercing.objects.create(
            nombre="Piercing Prueba",
            ubi="lobulo",
            precio=300,
            public=True
        )
        cls.piercing_private = Piercing.objects.create(
            nombre="Piercing Privado",
            ubi="helix",
            precio=400,
            public=False
        )
    
    def test_list_piercings(self):
        """Test para el listado general de piercings"""
        url = reverse('piercing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_public_piercings(self):
        """Test para el endpoint de piercings públicos"""
        url = reverse('piercing-publicos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica que solo devuelva los piercings públicos
        self.assertTrue(all(piercing['public'] for piercing in response.data))
    
    def test_create_piercing(self):
        """Test para creación de piercing (requiere autenticación)"""
        url = reverse('piercing-list')
        data = {
            'nombre': 'Nuevo Piercing',
            'ubi': 'tragus',
            'precio': 350,
            'public': True
        }
        # Aquí deberías agregar autenticación si es requerida
        # self.client.credentials(HTTP_AUTHORIZATION='Bearer token')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)