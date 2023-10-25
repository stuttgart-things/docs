# /GITHUB

## GITHUB ACTIONS ON K8S

[Deploying runner scale sets with Actions Runner Controller](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller#using-docker-in-docker-or-kubernetes-mode-for-containers)

<details open><summary><b>DEPLOY GHA SCALE SET CONTROLLER</b></summary>

```bash
helm upgrade --install arc \
--namespace arc-systems \
--create-namespace \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

</details close>

<details open><summary><b>DEPLOY OPENEBS</b></summary>

```bash
helm repo add openebs https://openebs.github.io/charts
helm install openebs openebs/openebs --version 3.9.0 -n openebs --create-namespace
```

</details close>

<details open><summary><b>DEPLOY K8S AUTOSCALINGRUNNERSET</b></summary>

```bash
cat <<EOF > ./k8s-arc-scale-values.yaml
containerMode:
  type: kubernetes
  kubernetesModeWorkVolumeClaim:
    accessModes: ["ReadWriteOnce"]
    storageClassName: openebs-hostpath
    resources:
      requests:
        storage: 1Gi

template:
  spec:
    containers:
    - name: runner
      image: ghcr.io/actions/actions-runner:latest
      command: ["/home/runner/run.sh"]
      env:
        - name: ACTIONS_RUNNER_REQUIRE_JOB_CONTAINER
          value: "false"
EOF

GITHUB_CONFIG_URL="https://github.com/stuttgart-things/docs"
GITHUB_PAT="<$GITHUB_PAT>"
helm upgrade --install k8s-docs \
--namespace arc-runners \
--create-namespace \
--set githubConfigUrl="${GITHUB_CONFIG_URL}" \
--set githubConfigSecret.github_token="${GITHUB_PAT}" \
--values ./k8s-arc-scale-values.yaml \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set --version 0.6.1
```

</details close>

<details open><summary><b>TEST PIPELINE</b></summary>

```yaml
name: ACTIONS RUNNER K8S SMOKE TEST
on:
  workflow_dispatch:

jobs:
  Smoke:
    runs-on: k8s-docs
    container: nginx:1.25.2-alpine
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - run: |
          echo "🎉 This job runs on kubernetes!"
          cat /etc/os-release
          ls -lta
```

</details close>

## GITHUB CLI

<details open><summary><b>CREATE PULL REQUEST</b></summary>

```bash
gh pr create -t "tekton-test1" -b "added git tasks to taskfile"
```

</details close>

<details open><summary><b>CREATE RELEASE</b></summary>

```bash
gh release create {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} --notes "released chart artifcact for {{ .PROJECT }}" {{ .PACKAGE }}
```

</details close>

<details open><summary><b>DELETE RELEASE</b></summary>

```bash
gh release delete {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} -y || true
```

</details close>

## GITHUB ACTIONS

### EXAMPLES

<details open><summary><b>test-workflow</b></summary>

```yaml
name: Actions Runner Controller Demo
on:
  workflow_dispatch:
jobs:
  Explore-GitHub-Actions:
    runs-on: arc-runner-set
    steps:
      - run: echo "🎉 This job uses runner scale set runners!"
```

</details close>

<details open><summary><b>workflow.yaml</b></summary>

```yaml
name: Run git workflow
on:
  workflow_dispatch:
    inputs:
      dev-cleanup:
        description: "Dev: Check to enable deletion of the deployment"
        required: false
        type: boolean
        default: false
  push:
    branches: [ main ]

# USE IN MAIN BRANCH ONLY
build-helm-staging:
  if: github.event.ref == 'refs/heads/main'
  name: Staging
  needs:
    - Init
  uses: ./.github/workflows/helm.yaml
  with:
    environment-name: dev
    cancel-concurrent: false
    branch-name: ${{ needs.Init.outputs.branch_name }}
  secrets: inherit

build-helm-production:
  name: Production
  needs:
    - Init
    - Linting-staging
  uses: ./.github/workflows/helm.yaml
  with:
    environment-name: production
    cancel-concurrent: true
    branch-name: ${{ needs.Init.outputs.branch_name }}
  secrets: inherit
```

</details close>

<details open><summary><b>helm-job.yaml</b></summary>

```yaml
on:
  workflow_call:
    inputs:
      environment-name:
        required: true
        type: string
      branch-name:
        required: true
        type: string
jobs:
  build-helm:
    environment: ${{ inputs.environment-name }}
    steps:
      - name: CHECKOUT GIT
        uses: actions/checkout@v4
      - name: SETUP HELMFILE
        uses: mamezou-tech/setup-helmfile@v1.2.0
```

</details close>

## GITCONFIG

<details open><summary><b>EXAMPLE CONFIG</b></summary>

```bash
cat ~/.gitconfig
[url "https://${USERNAME}:${PASSWORD}@codehub.sva.de"]
        insteadOf = https://codehub.sva.de
[user]
        name = Patrick Hermann
        email = patrick.hermann@sva.de

[url "https://${USERNAME}:${PASSWORD}@github.com/stuttgart-things/"]
        insteadOf = https://github.com/stuttgart-things/

[user]
        name = Patrick Hermann
        email = patrick.hermann@sva.de
```

</details close>

## HUGO MARKDOWN STATIC SITE GENERATOR

<details open><summary><b>CREATE HUGO SITE</b></summary>

```bash
export SITE_NAME=BLOG
nerdctl run --user $(id -u):$(id -g) --rm -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine new site ${SITE_NAME} > --format yaml
```

</details close>

<details open><summary><b>CLONE THEME + CREATE CONFIG</b></summary>

```bash
export SITE_NAME=BLOG
cd ${SITE_NAME}

git clone https://github.com/alex-shpak/hugo-book ${SITE_NAME}/themes/hugo-book

cat <<EOF > ${SITE_NAME}/config.yaml
baseURL: http://example.org/
languageCode: en-us
title: My New Hugo Site
theme: hugo-book
EOF
```

</details close>

<details open><summary><b>RUN HUGO SITE</b></summary>

```bash
export SITE_NAME=BLOG

# EXAMPLE SITE
cp -R themes/hugo-book/exampleSite/content.en/* ./content

nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd)/blog:/src klakegg/hugo:0.107.0-ext-alpine server
```

</details close>

<details open><summary><b>BUILD STATIC CONTENT</b></summary>

```bash
nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine --verbose --destination public
```

</details close>

<details open><summary><b>RUN/VIEW STATIC CONTENT W/ NGINX</b></summary>

```bash
sudo nerdctl run -it --rm -p 8080:80 --name web -v public/:/usr/share/nginx/html nginx
```

</details close>
