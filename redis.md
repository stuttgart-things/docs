# stuttgart-things/docs/redis

## REDISEARCH

<details><summary>LOGIN</summary>

```bash
FT._LIST # LIST ALL INDEXES
FT.DROPINDEX homerun DD # DROP INDEX
FT.SEARCH github "@system:github" # SEARCH FOR FILED SYSTEM
```

</details>

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

<details><summary>DELETE ALL KEYS</summary>

```bash
PASSWORD=""
PORT=5000
SERVER=localhost
redis-cli --scan --pattern "*" -h ${SERVER} -p ${PORT} -a ${PASSWORD} | xargs redis-cli -h ${SERVER} -p ${PORT} -a ${PASSWORD} del
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

</details>
