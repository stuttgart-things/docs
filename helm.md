# HELM

<details><summary><b>FUNCTION</b></summary>

```yaml
# ./<CHART>/templates/_helpers.tpl

{{- define "run" -}}
{{- $envVar := first . -}}
{{- $runName := index . 1 -}}
{{- $run := index . 2 -}}
---
apiVersion: tekton.dev/{{ $run.apiVersion | default "v1" }}
kind: {{ $run.kind | default "Pipeline" }}Run
metadata:
  name: {{ $run.name }}{{- if $run.addRandomDateToRunName }}-{{ now | date "060102-1504" }}{{- end }}
  namespace: {{ $run.namespace | default $envVar.Values.defaultNamespace }}
{{- if $run.annotations }}
  annotations:
  {{- range $key, $value := $run.annotations }}
    {{ $key }}: {{ $value | quote }}
{{- end }}{{- end }}
spec:
  {{ $run.kind | replace "Run" "" | lower | default "pipeline" }}Ref:
{{- if $run.ref }}
    name: {{ $run.ref }}
{{ else }}
    resolver: {{ $run.resolver }}
    params:
    {{- range $k, $v := $run.resolverParams }}
      - name: {{ $k }}
        value: {{ $v | quote -}}
    {{ end }}
{{ end }}
  workspaces:
  {{- range $k, $v := $run.workspaces }}
    - name: {{ $k }}
    {{- if eq $v.workspaceKind "csi" }}
      csi:
        driver: {{ $v.secretProviderDriver }}
        readOnly: true
        volumeAttributes:
          secretProviderClass: {{ $v.secretProviderClass }}{{ end }}
    {{- if eq $v.workspaceKind "volumeClaimTemplate" }}
      volumeClaimTemplate:
        spec:
          storageClassName: {{ $v.storageClassName }}
          accessModes:
          - {{ $v.accessModes }}
          resources:
            requests:
              storage: {{ $v.storage }}{{ end }}
  {{- if or (ne $v.workspaceKind "volumeClaimTemplate") }}{{- if or (ne $v.workspaceKind "csi") }}
    {{- if eq $v.workspaceKind "emptyDir" }}
      emptyDir: {}{{ else }}
      {{ $v.workspaceKind }}:
        {{ $v.workspaceKind | replace "persistentVolumeClaim" "claim" }}Name: {{ $v.workspaceRef }}{{ end }}{{ end }}
  {{ end }}{{ end }}
  params:
  {{- range $k, $v := $run.params }}
    - name: {{ $k }}
      value: {{ $v | quote -}}
  {{ end }}
  {{- if $run.listParams }}
  {{- range $k, $v := $run.listParams }}
    - name: {{ $k }}
      value:
      {{- range $v }}
        - {{ . | quote }}
      {{- end }}
  {{ end }}
  {{ end }}
{{- end }}

{{/*
stuttgart-things/patrick.hermann@sva.de/2022
*/}}

```

</details>

<details><summary><b>INCLUDE</b></summary>

```yaml
# ./<CHART>/templates/runs.yaml

{{ if .Values.enableRuns }}
{{- $envVar := . -}}
{{- range $runName, $runTpl := .Values.runs -}}
{{ include "run" (list $envVar $runName $runTpl) }}
{{ end -}}
{{ end }}
```

</details>

<details><summary><b>VALUES</b></summary>

```yaml
# ./<CHART>/values.yaml
---
enableRuns: true

runs:
  build-kaniko:
    name: build-kaniko-image-scaffolder
    addRandomDateToRunName: true
    namespace: tektoncd
    kind: Pipeline
    ref: build-kaniko-image
    params:
      gitRepoUrl: https://github.<ENT>.com/<USER>/scaffolder.git
      gitRevision: add-tekton-pipelinerun-template
      gitWorkspaceSubdirectory: /kaniko/scaffolder
      dockerfile: Dockerfile
      context: /kaniko/scaffolder
      image: akswkstekton.azurecr.io/scaffolder
      tag: v4
    workspaces:
      shared-workspace:
        workspaceKind: volumeClaimTemplate
        storageClassName: longhorn
        accessModes: ReadWriteMany
        storage: 2Gi
      dockerconfig:
        workspaceKind: csi
        secretProviderDriver: secrets-store.csi.k8s.io
        secretProviderClass: vault-kaniko-creds
      basic-auth:
        workspaceKind: csi
        secretProviderDriver: secrets-store.csi.k8s.io
        secretProviderClass: vault-git-creds
```

</details>


<details><summary><b>RENDER/INSTALL/APPLY</b></summary>

```bash
helm template <CHART>
helm upgrade --install test <CHART> -n test --create-namespace
helm template <CHART> | kubectl apply -f -
```

</details>