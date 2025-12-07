# merchants/auth.py
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework.exceptions import AuthenticationFailed

from .models import APIKey, hash_key


class ApiKeyAuthentication(BaseAuthentication):
    """
    Authenticate using an API key sent in either:
    - X-API-KEY: <raw_key>
    - Authorization: ApiKey <raw_key>
    """

    keyword = b"ApiKey"

    def authenticate(self, request):
        # 1) Try X-API-KEY header first
        raw_key = request.headers.get("X-API-KEY")

        # 2) If not present, try Authorization: ApiKey <key>
        if not raw_key:
            auth = get_authorization_header(request).split()
            if not auth or auth[0].lower() != self.keyword.lower():
                return None  # no API key here, let other auth classes try
            if len(auth) == 1:
                raise AuthenticationFailed("Invalid API key header. No credentials provided.")
            elif len(auth) > 2:
                raise AuthenticationFailed("Invalid API key header. Token string should not contain spaces.")
            raw_key = auth[1].decode("utf-8")

        if not raw_key:
            return None

        # Hash incoming key and look up
        hashed = hash_key(raw_key)

        try:
            api_obj = APIKey.objects.select_related("merchant", "merchant__owner").get(
                hashed_key=hashed, revoked=False
            )
        except APIKey.DoesNotExist:
            raise AuthenticationFailed("Invalid or revoked API key.")

        # Attach merchant to request for downstream use
        request.merchant = api_obj.merchant
        request.api_key = api_obj

        # DRF expects a (user, auth) tuple
        user = api_obj.merchant.owner
        return (user, None)
