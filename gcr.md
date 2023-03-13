# stuttgart-things/gcr

## LOGIN W/HELM AT GCR

```
cat gcr.json | helm registry login -u _json_key --password-stdin \eu.gcr.io
```

## PUSH OCI HELM CHART TO GCR
```
helm package ./sthings-helm-toolkit
helm push sthings-helm-toolkit-2.4.7.tgz oci://eu.gcr.io/stuttgart-things/sthings-helm-toolkit
```
## LOGIN W/NERDCTL AT GCR

```
cat gcr.json | nerdctl login -u _json_key --password-stdin \eu.gcr.io
```
