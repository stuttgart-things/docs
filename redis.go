# stuttgart-things/docs/redis

## REDIS-CLI
```
redis-cli -a ${REDIS_PASSWORD} # k8s redis inside pod
redis-cli -h redis-pve.labul.sva.de -a ${REDIS_PASSWORD} # remote redis
```

## LIST KEYS
```
KEYS *
```

## READ REDIS STREAM
```
XREAD COUNT 2 STREAMS redisqueue:yacht-revisionruns writers 0-0 0-0
```

Delete stream

```
DEL redisqueue:yacht-revisionruns writers 0-0 0-0
```

Get random member from set

```
SRANDMEMBER whatever 1
```

Get random member from set

```
SRANDMEMBER whatever 1
```
