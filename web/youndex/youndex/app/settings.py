SECRET_KEY = 'youwillneverguessthiskey123321123kasdkas'
REDIS_HOST = 'redis'
REDIS_PORT = '6379'
REDIS_DB = '0'
MONGODB_DB = 'youndex'
MONGODB_HOST = 'mongo'
MONGODB_PORT = 27017
FLAG = "shadowctf{yeap_we_love_ssrf_too}"
CELERY_BROKER_URL = 'redis://{host}:{port}/1'.format(host=REDIS_HOST, port=REDIS_PORT)
