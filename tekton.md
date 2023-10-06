# TEKTON

## PIPELINERUN EXAMPLES

<details><summary><b>LINT-GOLANG</b></summary>

```yaml
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: lint-scaffolder-cli-1
spec:
  pipelineRef:
    name: lint-golang-module
  workspaces:
    - name: source
      volumeClaimTemplate:
        spec:
          storageClassName: longhorn
          accessModes:
            - ReadWriteMany
          resources:
            requests:
              storage: 1Gi
    - name: secrets
      csi:
        driver: 'secrets-store.csi.k8s.io'
        readOnly: true
        volumeAttributes:
          secretProviderClass: vault-git-creds
    - name: basic-auth
      csi:
        driver: 'secrets-store.csi.k8s.io'
        readOnly: true
        volumeAttributes:
          secretProviderClass: vault-git-creds
  params:
    - name: gitRepoUrl
      value: https://github.<ENT>.com/<USERNAME>/scaffolder.git
    - name: gitRevision
      value: main
    - name: gitWorkspaceSubdirectory
      value: scaffolder
    - name: golintImage
      value: docker.io/golangci/golangci-lint:v1.54-alpine
```

</details>

## SECRET MANIFEST TEMPLATES

<details><summary><b>REGISTRY SECRET MANIFEST</b></summary>

```yaml
apiVersion: v1
data:
  config.json: <$(cat .docker/config.json | base64 -w 0)>
kind: Secret
metadata:
  name: acr
type: Opaque
```

</details>

<details><summary><b>BASIC AUTH SECRET MANIFEST</b></summary>

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: basic
type: Opaque
stringData:
  .gitconfig: |
    [url "https://<USERNAME>:<TOKEN>@github.<ENT>.com"]
        insteadOf = https://github.<ENT>.com
    [user]
        name = Patrick Hermann
        email = patrick.hermann@sva.de
  .git-credentials: |
    https://<USERNAME>:<TOKEN>@github.<ENT>.com
```

</details>

<details><summary><b>GITHUB TOKEN SECRET MANIFEST</b></summary>

```yaml
kind: Secret
apiVersion: v1
metadata:
  name: github-token
stringData:
  token: <TOKEN>
```

</details>
