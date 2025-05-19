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
        # Crear usuarios de prueba con diferentes roles
        cls.superuser = User.objects.create_user(
            username='hollow',
            password='2502',
            is_superuser=True
        )
        
        cls.perforador = User.objects.create_user(
            username='perforador',
            password='perforador123'
        )
        
        cls.tatuador = User.objects.create_user(
            username='tatuador',
            password='tatuador123'
        )
        
        cls.normal_user = User.objects.create_user(
            username='normal',
            password='normal123'
        )
        
        # Crear piercing de prueba
        cls.piercing = Piercing.objects.create(
            nombre="Piercing Prueba",
            ubi="lobulo",
            precio=300,
            public=True
        )

    def setUp(self):
        # Configurar autenticación por cookie (como en tu producción)
        self.client.cookies.load({'access_token': ''})

    def _auth_user(self, user):
        """Helper para autenticar usuario"""
        refresh = RefreshToken.for_user(user)
        self.client.cookies['access_token'] = str(refresh.access_token)

    # Tests para endpoints públicos
    def test_publicos_endpoint_unauthenticated(self):
        """Endpoint público debe funcionar sin autenticación"""
        url = reverse('piercing-publicos')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # Tests para superuser
    def test_create_piercing_as_superuser(self):
        """Superuser puede crear piercings"""
        self._auth_user(self.superuser)
        url = reverse('piercing-list')
        data = {
            'nombre': 'Piercing Superuser',
            'ubi': 'helix',
            'precio': 350,
            'public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Tests para perforador
    def test_create_piercing_as_perforador(self):
        """Perforador puede crear piercings"""
        self._auth_user(self.perforador)
        url = reverse('piercing-list')
        data = {
            'nombre': 'Piercing Perforador',
            'ubi': 'tragus',
            'precio': 400,
            'public': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Tests para tatuador (no debería tener permisos)
    def test_create_piercing_as_tatuador(self):
        """Tatuador NO puede crear piercings"""
        self._auth_user(self.tatuador)
        url = reverse('piercing-list')
        data = {
            'nombre': 'Piercing Tatuador',
            'ubi': 'rook',
            'precio': 450,
            'public': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Tests para usuario normal
    def test_create_piercing_as_normal_user(self):
        """Usuario normal NO puede crear piercings"""
        self._auth_user(self.normal_user)
        url = reverse('piercing-list')
        data = {
            'nombre': 'Piercing Normal',
            'ubi': 'daith',
            'precio': 500,
            'public': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Tests para métodos seguros (GET)
    def test_list_piercings_unauthenticated(self):
        """Listado de piercings debe ser accesible sin autenticación"""
        url = reverse('piercing-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)