import os

MANTLE_DEV_ALIAS = "dev"
MANTLE_STAGING_ALIAS = "staging"
MANTLE_PROD_ALIAS = "prod"
MANTLE_LOCAL_ALIAS = "local"

MANTLE_DEV_API = "https://dev.api.mantlebio.com"
MANTLE_STAGING_API = "https://staging.api.mantlebio.com"
MANTLE_PROD_API = "https://api.mantlebio.com"
MANTLE_LOCAL_API = "http://localhost:8080"

MANTLE_API_MAP = {
    MANTLE_DEV_ALIAS.upper(): MANTLE_DEV_API,
    MANTLE_STAGING_ALIAS.upper(): MANTLE_STAGING_API,
    MANTLE_PROD_ALIAS.upper(): MANTLE_PROD_API,
    MANTLE_LOCAL_ALIAS.upper(): MANTLE_LOCAL_API,
}
