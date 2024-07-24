import os

BUILTAPI_CLIENT_ID = os.getenv("BUILTAPI_CLIENT_ID")
BUILTAPI_CLIENT_SECRET = os.getenv("BUILTAPI_CLIENT_SECRET")
BUILTAPI_CLIENT_USER = os.getenv("BUILTAPI_CLIENT_USER")
BUILTAPI_CLIENT_PASSWORD = os.getenv("BUILTAPI_CLIENT_PASSWORD")
BUILTAPI_AUDIENCE = os.getenv("BUILTAPI_AUDIENCE", "https://gateway.builtapi.dev")
BUILTAPI_GATEWAY_URL = os.getenv("BUILTAPI_GATEWAY_URL", "https://gateway.builtapi.dev")
BUILTAPI_TOKEN_URL = os.getenv("BUILTAPI_TOKEN_URL", "https://builtapi-dev.eu.auth0.com/oauth/token")

GATEWAY_BASE_URL = "https://gateway.builtapi.dev"

MOCK_WORKSPACE_ID = "5b635842-d0e1-4c1b-8a77-af2046475897"
MOCK_ENTITY_ID = "1b635842-d0e2-4c1b-8a77-af2046475877"
MOCK_ENTITY_NAME = "mock-entity"
