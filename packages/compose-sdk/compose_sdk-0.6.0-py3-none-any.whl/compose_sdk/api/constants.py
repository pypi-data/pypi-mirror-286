WS_URL_PATH = "api/v1/sdk/ws"

WS_CLIENT = {
    "URL": {
        "DEV": f"ws://localhost:8080/{WS_URL_PATH}",
        "PROD": f"wss://app.composehq.com/{WS_URL_PATH}",
    },
    "RECONNECTION_INTERVAL": {
        "BASE_IN_SECONDS": 5,
        "BACKOFF_MULTIPLIER": 1.7,
    },
    "CONNECTION_HEADERS": {
        "API_KEY": "x-api-key",
        "PACKAGE_NAME": "x-package-name",
        "PACKAGE_VERSION": "x-package-version",
    },
    "ERROR_RESPONSE_HEADERS": {
        "REASON": "x-error-reason",
        "CODE": "x-error-code",
    },
}
