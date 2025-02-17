# stuttgart-things/docs/helm

## SNIPPETS

<details><summary><b>USECASE: KEYCLOAK DEPLOYMENT</b></summary>

```bash
cat <<EOF | kubectl apply -f -
---
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: keycloak
  namespace: keycloak
spec:
  commonName: keycloak.mycluster.lab.com
  dnsNames:
  - keycloak.mycluster.lab.com
  issuerRef:
    kind: ClusterIssuer
    name: cluster-issuer-approle
  secretName: keycloak.mycluster.lab.com-tls
EOF

cat <<EOF > keycloak-values.yaml
---
auth:
  adminUser: admin
  adminPassword: admin123 # Change this for security
proxy: edge # Useful for running Keycloak behind an Ingress or LoadBalancer
service:
  type: ClusterIP # Change to LoadBalancer if needed

extraEnvVars:
  - name: KEYCLOAK_LOG_LEVEL
    value: DEBUG
  - name: KEYCLOAK_EXTRA_ARGS
    value: "--import-realm"

global:
  defaultStorageClass: nfs4-csi
  storageClass: nfs4-csi
ingress:
  enabled: true
  ingressClassName: nginx
  hostname: keycloak.mycluster.lab.com
  tls: false
  extraTls:
    - hosts:
        - keycloak.mycluster.lab.com
      secretName: keycloak.mycluster.lab.com-tls

startupProbe:
  enabled: true
  failureThreshold: 30
  periodSeconds: 10
EOF

helm upgrade --install keycloak oci://registry-1.docker.io/bitnamicharts/keycloak --version 24.4.9 -n keycloak --create-namespace --values keycloak-values.yaml
```

</details>

<details><summary><b>USECASE: OPENLDAP CHART</b></summary>

```bash
# ADD HELM REPOSIORY + SEARCH FOR CHART/VERSION
helm repo add helm-openldap https://jp-gouin.github.io/helm-openldap/
helm repo update
helm search repo openldap
```

```bash
# GET DEFAULTS AS FILE
helm show values helm-openldap/openldap-stack-ha --version 4.3.1 > openldap-values.yaml
```

```bash
# USED VALUES
cat <<EOF > openldap-values.yaml
---
replicaCount: 1
replication:
  enabled: false
persistence:
  enabled: false
ltb-passwd:
  enabled : true
  ingress:
    enabled: true
    ingressClassName: nginx
    hosts:
    - "ssl-ldap2.mycluster.lab.com"
phpldapadmin:
  enabled: true
  ingress:
    enabled: true
    ingressClassName: nginx
    path: /
    hosts:
    - phpldapadmin.mycluster.lab.com
EOF
```

```bash
## HELM INSTALL
helm upgrade --install openldap helm-openldap/openldap-stack-ha --values openldap-values.yaml -n openldap --create-namespace
```

```bash
## REQUIREMENTS
sudo apt install ldap-utils -y
kubectl port-forward svc/openldap -n openldap 1389:389
```

## SEARCH

```bash
ldapsearch -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -b "dc=example,dc=org"
#Not@SecurePassw0rd
```

## CREATE GROUPS

```bash
cat <<EOF > ou_groups.ldif
dn: ou=groups,dc=example,dc=org
objectClass: organizationalUnit
ou: groups
EOF

cat <<EOF > group.ldif
dn: cn=developers,ou=groups,dc=example,dc=org
objectClass: top
objectClass: posixGroup
cn: developers
gidNumber: 1001
EOF
```

```bash
ldapadd -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -f ou_groups.ldif
ldapadd -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -f group.ldif
```

## CREATE USERS

```bash
cat <<EOF > user.ldif
dn: uid=johndoe,ou=users,dc=example,dc=org
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: inetOrgPerson
objectClass: posixAccount
objectClass: shadowAccount
uid: johndoe
cn: John Doe
sn: Doe
mail: johndoe@example.com
uidNumber: 1001
gidNumber: 1001
homeDirectory: /home/johndoe
loginShell: /bin/bash
userPassword: {SSHA}gprTucQeJjW+66qAGkmShgQ3IJrwY0ER
EOF
```

```bash
# CREATE PASSWORD
slappasswd -h {SSHA} -s hallobibi
ldapadd -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -f user.ldif 
```

## ADD USER TO GROUP

```bash
cat <<EOF > group_modify.ldif
dn: cn=developers,ou=groups,dc=example,dc=org
changetype: modify
add: memberUid
memberUid: johndoe
EOF
```

```bash
ldapmodify -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -f group_modify.ldif
````

```bash
## SEARCH USERS
ldapsearch -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -b "dc=example,dc=org" # GENERAL
ldapsearch -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -b "dc=example,dc=org" "(objectClass=posixAccount)"
ldapsearch -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -b "dc=example,dc=org" "(objectClass=posixGroup)"
ldapsearch -x -H ldap://localhost:1389 -D "cn=admin,dc=example,dc=org" -W -b "dc=example,dc=org" "(&(objectClass=posixGroup)(cn=developers))" memberUid

## SEARCH SCHEMA
ldapsearch -x -H ldap://10.31.101.9:389 -D "cn=admin,dc=charite,dc=de" -W -b "cn=subschema" -s base "(objectclass=*)" attributeTypes
```

```python
# PYTHON LDAP USER LOGIN TEST SCRIPT
cat <<EOF > ldap_login.py
import os
from ldap3 import Server, Connection, ALL, SIMPLE
import getpass

# LDAP Server Configuration
LDAP_SERVER = "ldap://localhost:1389"  # Change to your LDAP server
BASE_DN = "dc=example,dc=org"  # Adjust to match your LDAP structure
USER_DN_FORMAT = "uid={},ou=users," + BASE_DN  # Adjust based on your LDAP structure

# Retrieve Admin Credentials from Environment Variables
ADMIN_DN = "cn=admin," + BASE_DN
ADMIN_PASSWORD = os.getenv("LDAP_ADMIN_PASSWORD", "fallback-password")  # Use a secure method

def authenticate(username, password):
    """ Authenticate user against the LDAP server """
    user_dn = USER_DN_FORMAT.format(username)
    try:
        conn = Connection(LDAP_SERVER, user=user_dn, password=password, authentication=SIMPLE, auto_bind=True)
        print("[✅] Authentication successful for user:", username)
        conn.unbind()
        return True
    except Exception as e:
        print("[❌] Authentication failed:", e)
        return False

def search_user(username):
    """ Search for a user in LDAP """
    try:
        server = Server(LDAP_SERVER, get_info=ALL)
        conn = Connection(server, ADMIN_DN, ADMIN_PASSWORD, auto_bind=True)

        search_filter = f"(uid={username})"
        conn.search(BASE_DN, search_filter, attributes=['cn', 'mail'])

        if conn.entries:
            print(f"[🔍] Found user: {conn.entries[0]}")
        else:
            print("[⚠️] User not found.")

        conn.unbind()
    except Exception as e:
        print("[❌] Error searching for user:", e)

if __name__ == "__main__":
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    if authenticate(username, password):
        search_user(username)  # Optional: Retrieve user details
    else:
        print("Login failed. Please try again.")
EOF
```

```bash
pip install ldap3 
export LDAP_ADMIN_PASSWORD="Not@SecurePassw0rd"
python3 ldap_login.py
```

</details>

<details><summary><b>GET INSTALLED MANIFESTS BY RELEASE</b></summary>

```bash
helm get manifest ghr-install-configure-docker-sthings-cicd -n arc-runners
```

</details>

<details><summary><b>USAGE HELM-TOOLKIT</b></summary>

```bash
CHART_NAME=test-chart

mkdir -p ${CHART_NAME}/templates

cat <<EOF > ${CHART_NAME}/Chart.yaml
apiVersion: v2
name: ${CHART_NAME}
description: A Helm chart for Kubernetes
type: application
version: v0.1.0
appVersion: v0.1.0
dependencies:
  - name: sthings-helm-toolkit
    version: 2.4.74
    repository: oci://eu.gcr.io/stuttgart-things
EOF

cat <<EOF > ${CHART_NAME}/values.yaml
---
EOF

cd ${CHART_NAME}
helm dep update
```

what (library) templates should be included in the templates dir?
- everything which the chart can/should be render (= the app should support)

-> example: we provide ingress, custom-resource in the chart but we will not add values for it. the user can use it later by adding values to it but those values are (mostly) depending on a env and therefor non default for an application.

```bash
helm upgrade --install homerun-light-mock . -n homerun-light-mock --create-namespace --set namespace=homerun-light-mock
```

```bash
helm uninstall homerun-light-mock -n homerun-light-mock
```

```bash
helmfile template k8s/helmfile.yaml -e homerun-dev
```

</details>

<details><summary><b>RENDER/INSTALL/APPLY</b></summary>

```bash
helm template <CHART>
helm upgrade --install test <CHART> -n test --create-namespace
helm template <CHART> | kubectl apply -f -
```

</details>

<details><summary>STATUS</summary>

```bash
helm status vault -n vault
helm get manifest vault -n vault
```

</details>

<details><summary>HELM PACKAGE</summary>

```bash
helm package <DIR-TO-HELM-CHART>
```

</details>

<details><summary>HELM REGISTRY LOGIN</summary>

```bash
helm registry login -u sthings -p <REPLACE-ME> scr.tiab.labda.sva.de
```

</details>

<details><summary>PUSH CHART TO HARBOR</summary>

```bash
helm push sthings-demo-news-0.1.0.tgz oci://scr.tiab.labda.sva.de/sthings-k8s-operator/
```

</details>

<details><summary>PULL CHART FROM HARBOR</summary>

```bash
helm pull oci://scr.tiab.labda.sva.de/sthings-k8s-operator/sthings-demo-news --version 0.1.0
```

</details>

<details><summary>INSTALL CHART FROM OCI/HARBOR</summary>

```bash
helm install --upgrade sthings-operator oci://scr.tiab.labda.sva.de/sthings-k8s-operator/sthings-demo-news --version 0.1.0
```

</details>

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

## HELMFILE

<details><summary>SET VAULT CONNECTION</summary>

```bash
export VAULT_ADDR=https://${VAULT_FQDN}}
export VAULT_NAMESPACE=root

# APPROLE AUTH
export VAULT_AUTH_METHOD=approle
export VAULT_ROLE_ID=${VAULT_ROLE_ID}
export VAULT_SECRET_ID=${VAULT_SECRET_ID}

# TOKEN AUTH
export VAULT_AUTH_METHOD=token #default
export VAULT_TOKEN=${VAULT_TOKEN}
```

</details>

<details><summary>RENDER/APPLY</summary>

```bash
helmfile template --environment labul-pve-dev
helmfile sync --environment labul-pve-dev
```

</details>

<details><summary> TEST REGISTRY SECRETS W/ HELM</summary>

```bash
kubectl run helm-pod -it --rm --image alpine/k8s:1.24.15 -- sh

mkdir -p ~/.docker/
cat <<EOF > ~/.docker/config.json
{"auths": #...
EOF

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm pull bitnami/nginx --version 15.1.0
tar xvfz nginx-15.1.0.tgz
yq e -i '.version = "9.9.9"' nginx/Chart.yaml
helm package nginx
helm push nginx-9.9.9.tgz oci://eu.gcr.io/stuttgart-things/
```

</details>
