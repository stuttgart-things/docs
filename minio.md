# stuttgart-things/docs/minio

## MC COMMAND SNIPPETS

```bash
mc anonymous set public artifacts-labda/roles # SET BUCKET TO PUBLIC
mc ls artifacts-labda # LIST BUCKETS
```

## MC CONFIG (EXAMPLE)

```json
cat ~/.mc/config.json
{
        "version": "10",
        "aliases": {
                "artifacts-labda": {
                        "url": "https://artifacts.app.4sthings.tiab.ssc.sva.de",
                        "accessKey": "sthings",
                        "secretKey": "",
                        "api": "s3v4",
                        "path": "auto"
                } #,..
}
```
