# app/api/viewsets/auth.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from app.api.permissions import JWTAuthenticationFromCookie

class AuthViewSet(viewsets.ViewSet):
    """Login / Logout / Check usando JWT en cookies."""
    authentication_classes = [JWTAuthenticationFromCookie]
    permission_classes     = [IsAuthenticated]

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        remember = request.data.get('remember', False)

        # Autentica usuario
        from django.contrib.auth import authenticate
        user = authenticate(request, username=username, password=password)
        if user is None:
            return Response(
                {'detail': 'Credenciales inválidas'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Crea tokens
        refresh = RefreshToken.for_user(user)
        access  = str(refresh.access_token)
        refresh = str(refresh)

        # Prepara respuesta
        resp = Response({
            'detail': 'Autenticado correctamente',
            'user': user.username
        }, status=status.HTTP_200_OK)

        # Configuración de expiración
        if remember:
            # usa los lifetimes por defecto de SimpleJWT
            access_max_age  = None
            refresh_max_age = None
        else:
            # expire al cerrar navegador
            access_max_age  = None
            refresh_max_age = None
            # si quisieras caducar al cerrar, podrías no setear expires

        # Setea cookies HttpOnly+Secure
        resp.set_cookie(
            'access_token', access,
            httponly=True,
            secure=True,
            samesite='None',
            path='/api/'
        )
        resp.set_cookie(
            'refresh_token', refresh,
            httponly=True,
            secure=True,
            samesite='None',
            path='/api/token/refresh/'
        )
        return resp

    @action(detail=False, methods=['post'])
    def logout(self, request):
        # Opcionalmente blacklist del refresh
        from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
        try:
            refresh = request.COOKIES.get('refresh_token')
            token   = RefreshToken(refresh)
            token.blacklist()
        except Exception:
            pass

        # Borra cookies
        resp = Response(
            {'detail': 'Desconectado correctamente'},
            status=status.HTTP_200_OK
        )
        resp.delete_cookie('access_token', path='/api/')
        resp.delete_cookie('refresh_token', path='/api/token/refresh/')
        return resp

    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def check(self, request):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return Response({'authenticated': False}, status=status.HTTP_200_OK)

        # Tipo de usuario
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
