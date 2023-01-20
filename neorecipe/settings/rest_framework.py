import environ

env = environ.Env()
environ.Env.read_env()

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': env.int('NEORECIPE_DEFAULT_PAGE_SIZE', 25),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': env.str('NEORECIPE_THROTTLE_LIMIT_ANON', '100/minute'),
        'user': env.str('NEORECIPE_THROTTLE_LIMIT_USER', '100/minute'),
    },
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

REST_FRAMEWORK_DEBUG = {
    
}

if env.bool('NEORECIPE_DEBUG_ENABLED', default=False) == True:
    REST_FRAMEWORK.update(REST_FRAMEWORK_DEBUG)