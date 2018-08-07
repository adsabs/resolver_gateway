import logging
LOG_LEVEL = 30 # To be deprecated when all microservices use ADSFlask
LOGGING_LEVEL = "INFO"
LOG_STDOUT = True
DISCOVERER_SELF_PUBLISH = True
GATEWAY_RESOLVER_SERVICE_URL = "https://qa.adsabs.harvard.edu/v1/resolver/%s"
GATEWAY_SERVICE_ACCOUNT_INFO_URL = ""
GATEWAY_TOKEN = ""
REDIS_URL = ""


# added by eb-deploy (over-write config values) from environment
try:
    import os, json, ast
    G = globals()
    for k, v in os.environ.items():
        if k == k.upper() and k in G:
            logging.info("Overwriting constant '%s' old value '%s' with new value '%s'", k, G[k], v)
            try:
                w = json.loads(v)
                G[k] = w
            except:
                try:
                    # Interpret numbers, booleans, etc...
                    G[k] = ast.literal_eval(v)
                except:
                    # String
                    G[k] = v
except:
    pass
