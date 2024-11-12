
CLIENT_ID = "airflow"
CLIENT_SECRET = "gPkYvPgUh10miAJwGljYDAmy4rIuzxrT"
OIDC_ISSUER = "http://192.168.10.171:8890/realms/kc-thaibinh"

PROVIDER_NAME = "keycloak"
OIDC_BASE_URL = "{oidc_issuer}/protocol/openid-connect".format(oidc_issuer=OIDC_ISSUER)
OIDC_TOKEN_URL = "{oidc_base_url}/token".format(oidc_base_url=OIDC_BASE_URL)
OIDC_AUTH_URL = "{oidc_base_url}/auth".format(oidc_base_url=OIDC_BASE_URL)