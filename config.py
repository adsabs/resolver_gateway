LOG_STDOUT = False
LOGGING_LEVEL = 'DEBUG'

# This the URL to resolver_service api
GATEWAY_RESOLVER_SERVICE_URL = 'https://dev.adsabs.harvard.edu/v1/resolver/%s'

# This is a URL to adsws account info service
GATEWAY_SERVICE_ACCOUNT_INFO_URL = ''

# gateway token
GATEWAY_TOKEN = 'this is a secret api token!'

# For caching
REDIS_URL = "redis://localhost:6379/0"
REDIS_NAME_PREFIX = "link_gateway_"
# save to cache for a week
REDIS_EXPIRATION_TIME = 604800

GATEWAY_SERVICE_REFERRED_DOMAIN = 'adsabs.harvard.edu'

GATEWAY_ADS_ABSTRACT_PAGE = '/abs/%s/abstract'
