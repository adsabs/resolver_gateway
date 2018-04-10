
# These are the URL and token for resolver_service api
RESOLVER_SERVICE_URL = 'https://dev.adsabs.harvard.edu/v1/resolver/%s'
RESOLVER_SERVICE_ADSWS_API_TOKEN = 'this is a secret api token!'

# Service URL to translate session into user account information
ACCOUNT_TOKEN_SERVICE_URL = 'https://dev.adsabs.harvard.edu/v1/account/token'

# Redis URL for caching sessions
REDIS_URL = "redis://localhost:6379/0"
REDIS_PREFIX = "SESSION_CACHE"
