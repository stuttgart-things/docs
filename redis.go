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
