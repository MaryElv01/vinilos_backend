from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from app.models import Piercing
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class PiercingEndpointTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear usuario de prueba
        cls.user = User.objects.create_user(
            username='hollow',
            password='2502',
            is_staff=True
        )
        
        # Crear piercings de prueba
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
    
    def setUp(self):
        # Obtener token JWT para autenticación
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.cookies['access_token'] = self.access_token
    
    def test_list_piercings_authenticated(self):
        """Test para el listado general de piercings (autenticado)"""
        url = reverse('piercing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
    
    def test_public_piercings_unauthenticated(self):
        """Test para endpoint público sin autenticación"""
        url = reverse('piercing-publicos')
        self.client.cookies = {}  # Limpiar cookies
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(piercing['public'] for piercing in response.data))
    
    def test_create_piercing_authenticated(self):
        """Test para creación de piercing (autenticado)"""
        url = reverse('piercing-list')
        data = {
            'nombre': 'Nuevo Piercing',
            'ubi': 'tragus',
            'precio': 350,
            'public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_piercing_unauthenticated(self):
        """Test para creación sin autenticación debe fallar"""
        url = reverse('piercing-list')
        self.client.cookies = {}  # Limpiar cookies
        data = {
            'nombre': 'Piercing No Auth',
            'ubi': 'daith',
            'precio': 400,
            'public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)