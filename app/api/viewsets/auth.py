from django.contrib.auth import authenticate, login, logout
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from app.api.permissions import CsrfExemptSessionAuthentication

class AuthViewSet(viewsets.ViewSet):
    # Usar la autenticación sin CSRF
    authentication_classes = [CsrfExemptSessionAuthentication]
    # Por defecto sólo usuarios autenticados, excepto donde digamos lo contrario
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        remember = request.data.get('remember', False)

        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)
        # si no hay “remember”, la sesión expira al cerrar navegador
        if not remember:
            request.session.set_expiry(0)

        return Response({
            'detail': 'Autenticado correctamente',
            'user': user.username
        }, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def logout(self, request):
        logout(request)
        return Response(
            {'detail': 'Desconectado correctamente'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'authenticated': False},
                status=status.HTTP_200_OK
            )

        user = request.user
        if user.is_superuser:
            tipo = 'administrador'
        elif user.username.lower() == 'tatuador':
            tipo = 'tatuador'
        elif user.username.lower() == 'perforador':
            tipo = 'perforador'
        else:
            tipo = None

        return Response({
            'authenticated': True,
            'user': user.username,
            'tipo_user': tipo
        }, status=status.HTTP_200_OK)