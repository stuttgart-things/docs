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

## READ STREAM
```
XREAD COUNT 2 STREAMS redisqueue:yacht-revisionruns writers 0-0 0-0
```

## DELETE STREAM

```
DEL redisqueue:yacht-revisionruns writers 0-0 0-0
```

## GET 1 RANDOM MEMBER FROM SET

```
SRANDMEMBER whatever 1
```

## GET JSON

```
JSON.GET st-0-execute-ansible-smt40-rke2-15-1717483c5a
```
