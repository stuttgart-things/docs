# /GIT

## GITHUB ACTIONS ON K8S

<details open><summary><b>DEPLOY GHA SCALE SET CONTROLLER</b></summary>

```bash
NAMESPACE="arc-systems"
helm upgrade --install arc \
--namespace "${NAMESPACE}" \
--create-namespace \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

</details close>

<details open><summary><b>DEPLOY GHA SCALE SET</b></summary>

```bash
INSTALLATION_NAME="docs-runner-set"
NAMESPACE="arc-runners"
GITHUB_CONFIG_URL="https://github.com/stuttgart-things/docs"
GITHUB_PAT="<$GITHUB_PAT>"

helm install --upgrade "${INSTALLATION_NAME}" \
--namespace "${NAMESPACE}" \
--create-namespace \
--set githubConfigUrl="${GITHUB_CONFIG_URL}" \
--set githubConfigSecret.github_token="${GITHUB_PAT}" \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set
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
  
```
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

