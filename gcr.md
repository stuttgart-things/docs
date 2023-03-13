# stuttgart-things/gcr

## LOGIN W/HELM AT GCR

```
cat gcr.json | helm registry login -u _json_key --password-stdin \eu.gcr.io
```

## LOGIN W/NERDCTL AT GCR

```
cat gcr.json | nerdctl login -u _json_key --password-stdin \eu.gcr.io
```
