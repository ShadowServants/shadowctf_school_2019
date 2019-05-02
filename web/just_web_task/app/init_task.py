from redis import Redis

redis_client = Redis(
    host='redis',
    port='6379',
    db=0
)

redis_client.hset('secrets', 'admin', 'shadowctf{jwt_brute_isnt_smart_but_works}')
redis_client.hset('passwords', 'admin', 'nopenopenope123321')
