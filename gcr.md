# stuttgart-things/docs/gcr

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

## ADD GCR TO HARBOR (REGISTRY)

Endpoint: https://eu.gcr.io
Access ID: _json_key

Access Secret:
```
{
  "type": "service_account",
  "project_id": "",
  "private_key_id": "",
  "private_key": "",
  "client_email": "",
  "client_id": "",
  "auth_uri": "",
  "token_uri": "",
  "auth_provider_x509_cert_url": "",
  "client_x509_cert_url": ""
}
```
