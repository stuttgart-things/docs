# stuttgart-things/docs/redis

## CLI

<details><summary>LOGIN</summary>

```bash
redis-cli -a ${REDIS_PASSWORD} # k8s redis inside pod
redis-cli -h redis-pve.labul.sva.de -a ${REDIS_PASSWORD} # remote redis
```

</details>

<details><summary>KEYS</summary>

```bash
KEYS *
```

</details>

<details><summary>STREAMS</summary>

```bash
# READ STREAM - EXAMPLE
XREAD COUNT 2 STREAMS redisqueue:yacht-revisionruns writers 0-0 0-0
# DELETE STREAM - EXAMPLE
DEL redisqueue:yacht-revisionruns writers 0-0 0-0
```

</details>

<details><summary>SETS</summary>

```bash
# GET 1 RANDOM MEMBER FROM SET
SRANDMEMBER whatever 1
```

</details>

<details><summary>JSON</summary>

```bash
JSON.GET st-0-execute-ansible-smt40-rke2-15-1717483c5a
```
