from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        # anulamos la comprobación de CSRF
        return

class JWTAuthenticationFromCookie(JWTAuthentication):
    """
    Lee el access token desde la cookie 'access_token'
    en vez de buscarlo en Authorization: Bearer <token>
    """
    def authenticate(self, request):
        raw_token = request.COOKIES.get('access_token')
        if not raw_token:
            return None
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token