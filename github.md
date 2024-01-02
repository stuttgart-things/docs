# stuttgart-things/docs/github

<!-- https://www.thisdot.co/blog/creating-your-own-github-action-with-typescript -->

## GITHUB ACTIONS ON K8S

<details><summary>INSTALL OPERATOR SDK</summary>

[Deploying runner scale sets with Actions Runner Controller](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller#using-docker-in-docker-or-kubernetes-mode-for-containers)

</details>

<details><summary>DEPLOY GHA SCALE SET CONTROLLER</summary>

```bash
helm upgrade --install arc \
--namespace arc-systems \
--create-namespace \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

</details>


</details close>

<details><summary>DEPLOY OPENEBS</summary>

```bash
helm repo add openebs https://openebs.github.io/charts
helm install openebs openebs/openebs --version 3.9.0 -n openebs --create-namespace
```

</details close>

<details><summary>DEPLOY K8S AUTOSCALINGRUNNERSET</summary>

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

<details><summary>TEST PIPELINE</summary>

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

<details><summary>CREATE PULL REQUEST</summary>

```bash
gh pr create -t "tekton-test1" -b "added git tasks to taskfile"
```

</details close>

<details><summary>CREATE RELEASE</summary>

```bash
gh release create {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} --notes "released chart artifcact for {{ .PROJECT }}" {{ .PACKAGE }}
```

</details close>

<details><summary>DELETE RELEASE</summary>

```bash
gh release delete {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} -y || true
```

</details close>

<details><summary>AUTO MERGE/REBASE PR</summary>

```bash
# GET LATEST PR AND AUTO MERGE + DELETE BRANCH
gh pr merge $(gh pr list | grep "^[^#;]" | awk '{print $1}') --auto --rebase --delete-branch
```

</details close>


## GITHUB ACTIONS

### EXAMPLES

<details><summary>TEST-WORKFLOW</summary>

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

<details><summary>MULTIPLE CHOICE INPUTS</summary>

```yaml
on:
  workflow_dispatch:
    inputs:
      name:
        type: choice
        description: Who to greet
        options:
          - maypayne
          - scorseese
          - deniro
jobs:
  greet:
    runs-on: ubuntu-latest
    steps:
    - name: Send greeting
      run: echo ${{ github.event.inputs.name }}"
```

</details close>



<details><summary>DEFAULTS FOR INPUTS</summary>

```yaml
# FOR EXAMPLE WHEN USING WORFLOW DISPATCH AND GIT TRIGGERS TO SET A DEFAULT VALUE
  - name: Set default value
    id: defaultname
    run: |
      USER_INPUT=${{ github.event.inputs.name }}
      echo "value=${USER_INPUT:-"Octocat"}" >> "$GITHUB_OUTPUT"

  - name: Do something with it
    run: |
      name="${{ steps.defaultname.outputs.value }}"
      echo "Name: $name"
```

</details close>

<details><summary>WORKFLOW</summary>

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

<details><summary>helm-job.yaml</summary>

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

<details><summary>EXAMPLE CONFIG</summary>

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

<details><summary>CREATE HUGO SITE</summary>

```bash
export SITE_NAME=BLOG
nerdctl run --user $(id -u):$(id -g) --rm -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine new site ${SITE_NAME} > --format yaml
```

</details close>

<details><summary>CLONE THEME + CREATE CONFIG</summary>

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

<details><summary>RUN HUGO SITE</summary>

```bash
export SITE_NAME=BLOG

# EXAMPLE SITE
cp -R themes/hugo-book/exampleSite/content.en/* ./content

nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd)/blog:/src klakegg/hugo:0.107.0-ext-alpine server
```

</details close>

<details><summary>BUILD STATIC CONTENT</summary>

```bash
nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine --verbose --destination public
```

</details close>

<details><summary>RUN/VIEW STATIC CONTENT W/ NGINX</summary>

```bash
sudo nerdctl run -it --rm -p 8080:80 --name web -v public/:/usr/share/nginx/html nginx
```

</details close>

<details><summary>YAML LINT</summary>

```bash
nerdctl run -it -v ./docs:/manifests cytopia/yamllint -- /manifests
```

</details close>
