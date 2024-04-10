# stuttgart-things/docs/github

<!-- https://www.thisdot.co/blog/creating-your-own-github-action-with-typescript -->

<!--
https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners-with-actions-runner-controller/deploying-runner-scale-sets-with-actions-runner-controller#using-docker-in-docker-or-kubernetes-mode-for-containers -->

## GITHUB ACTIONS ON K8S

<details><summary>DEPLOY GHA SCALE SET CONTROLLER</summary>

```bash
helm upgrade --install arc \
--namespace arc-systems \
--create-namespace \
oci://ghcr.io/actions/actions-runner-controller-charts/gha-runner-scale-set-controller
```

</details>

<details><summary>DEPLOY OPENEBS</summary>

```bash
helm repo add openebs https://openebs.github.io/charts
helm install openebs openebs/openebs --version 3.9.0 -n openebs --create-namespace
```

</details>

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

</details>

## GITHUB CLI

<details><summary>PUSH IMAGE TO GHCR</summary>

```bash
sudo nerdctl login ghcr.io -u patrick-hermann-sva -p $GITHUB_TOKEN
sudo nerdctl build -t ghcr.io/stuttgart-things/sthings-slides:v2 .
sudo nerdctl push ghcr.io/stuttgart-things/sthings-slides:v2
```

</details>

<details><summary>CREATE PULL REQUEST</summary>

```bash
gh pr create -t "tekton-test1" -b "added git tasks to taskfile"
```

</details>

<details><summary>CREATE REPOSITORY</summary>

```bash
gh repo create stuttgart-things/stagetime-operator \
--public \
--add-readme \
--description "stagetime operator" \
--clone \
--license Apache-2.0 \
-g Go
```

</details>

<details><summary>LIST AVAILABLE GITIGNORE TEMPLATES</summary>

```bash
gh api /gitignore/templates -q ".[]"
```

</details>

<details><summary>MERGE PULL REQUEST</summary>

```bash
gh pr merge $(gh pr list | grep "^[^#;]" | awk '{print $1}') --auto --rebase --delete-branch
```

</details>

<details><summary>CREATE RELEASE</summary>

```bash
gh release create {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} --notes "released chart artifcact for {{ .PROJECT }}" {{ .PACKAGE }}
```

</details>

<details><summary>DELETE RELEASE</summary>

```bash
gh release delete {{ .PROJECT }}-{{ .VERSION_NUMBER_PREFIX }}{{ .UPDATED_VERSION_NUMBER }} -y || true
```

</details>

<details><summary>AUTO MERGE/REBASE PR</summary>

```bash
# GET LATEST PR AND AUTO MERGE + DELETE BRANCH
gh pr merge $(gh pr list | grep "^[^#;]" | awk '{print $1}') --auto --rebase --delete-branch
```

</details>

## GITHUB ACTIONS

<details><summary>TEST WORKFLOW</summary>

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

</details>

<details><summary>USE OUTPUTS FROM JOBS IN REUSABLE WORKFLOWS</summary>

### REUSABLE WORFLOW (SHORTENED, WF WHICH WILL BE CALLED)

```yaml
---
name: Build ansible collection
on:
  workflow_call:
    inputs:
      runs-on:
        required: true
        type: string
    outputs:
      collection-version:
        description: version of ansible collection
        value: ${{ jobs.Ansible-Collection-Build.outputs.version }}
      artifact-name:
        description: name of uploaded ansible collection package
        value: ${{ jobs.Ansible-Collection-Build.outputs.artifact }}

jobs:
  Ansible-Collection-Build:
    outputs:
      version: ${{ steps.version.outputs.version }}
      artifact: ${{ steps.build.outputs.artifact }}
    runs-on: ${{ inputs.runs-on }}
    container:
      image: ${{ inputs.ansible-image }}
    environment: ${{ inputs.environment-name }}
    continue-on-error: ${{ inputs.continue-error }}
    steps:
      - name: Checkout code
        id: git
        uses: actions/checkout@v4.1.1
        with:
          path: source
          fetch-depth: "0"

      - id: version
        run: echo "version=$(yq -r '.version' source/${{ inputs.collection-file }})" >> "$GITHUB_OUTPUT"
        shell: bash
```

### WORFLOW (SHORTENED, WF WHICH CALLS THE REUSABLE WORKFLOW)

```yaml
---
name: Build Collection
on:
  workflow_dispatch:
    inputs:
      runs-on:
        type: string
        required: false
        default: ghr-deploy-configure-rke-cicd
      environment-name:
        type: string
        required: true
        default: k8s

jobs:
  Build-Collection:
    name: Build Ansible Collection
    uses: stuttgart-things/stuttgart-things/.github/workflows/ansible-collection.yaml@main
    with:
      runs-on: ${{ inputs.runs-on }}
      environment-name: ${{ inputs.environment-name }}
      continue-error: false

  Release-Collection:
    name: Release-Collection
    needs: Build-Collection
    permissions:
      contents: write
      pull-requests: write
    runs-on: ${{ inputs.runs-on }}
    environment: ${{ inputs.environment-name }}
    container:
      image: eu.gcr.io/stuttgart-things/machineshop:v1.7.2
    steps:
      - name: Download artifact
        id: download
        uses: actions/download-artifact@v4.1.4
        with:
          name: ${{ inputs.vm-name }}

      - name: Release module
        uses: ncipollo/release-action@v1.14.0
        with:
          name: ${{ needs.Build-Collection.outputs.artifact-name }}
          artifacts: ${{ needs.Build-Collection.outputs.artifact-name }}
          body: "ansible-collection"
          tag: ${{ needs.Build-Collection.outputs.collection-version }}
```

</details>

<details><summary>UPLOAD ARTIFACTS</summary>

```yaml
- name: Upload collection
  id: upload
  uses: actions/upload-artifact@v4.1.0
  with:
    name: ${{ env.COLLECTION_PACKAGE }}
    #path: ${{ github.workspace }}/*tar.gz*
    path: ${{ env.COLLECTION_PACKAGE_PATH }}
```

</details>

<details><summary>GITHUB EVENT DATA IN WORKFLOW</summary>

```yaml
#...
- name: Print Title of PR
  run: echo The Title of your PR is ${{ github.event.pull_request.title }}
- name: Print branch name
  run: echo The branch name from of your PR is ${{ github.event.pull_request.head.ref }}
# ..
```

</details>

<details><summary>SET ENV OUTPUTS</summary>

```yaml
# STEP1
# SET WORKING DIRS AS ENV-VARS
echo "COLLECTION_FILEPATH=source/${{ inputs.collection-file }}" >> $GITHUB_ENV
echo "COLLECTION_ROLES_DIR=$GITHUB_WORKSPACE/$(yq -r ".namespace" source/${{ inputs.collection-file }})/$(yq -r ".name" source/${{ inputs.collection-file }})/roles" >> $GITHUB_ENV
```

```yaml
# STEP2
# USE ENV VARS
count_plays=$(yq '.playbooks | keys' ${{ env.COLLECTION_FILEPATH }} | wc -l)
# ..
yq ".playbooks[$COUNTER].name" ${{ env.COLLECTION_FILEPATH }}
```

</details>

<details><summary>K8S WORKFLOW-EXAMPLE</summary>

```yaml
---
name: Build & Verify Terraform Module
on:
  workflow_dispatch:
  push:
    branches:
      - "main"

jobs:
  Terraform-Validate:
    runs-on: arc-runner-scale-set-vault-base-setup
    container:
      image: hashicorp/terraform:1.6
    environment: k8s
    continue-on-error: false
    steps:
      - name: Checkout code
        uses: actions/checkout@v4.1.1
      - run: |
          terraform init
          terraform fmt
          terraform validate
```

</details>

<details><summary>DISPATCH/INPUTS/USES EXAMPLE</summary>

```yaml
---
name: Release Terraform
on:
  workflow_dispatch:
    inputs:
      release-tag:
        required: true
        type: string
      release-message:
        required: true
        type: string

jobs:
  release-terraform:
    if: github.event.ref == 'refs/heads/main'
    name: Valdiate
    uses: stuttgart-things/stuttgart-things/.github/workflows/release-terraform.yaml@main
    with:
      module-name: vsphere-vm
      tag-name: "${{ github.event.inputs.release-tag }}"
      release-message: "${{ github.event.inputs.release-message }}"
      environment-name: k8s
      runs-on: arc-runner-scale-set-vsphere-vm
      continue-error: false
```

</details>

<details><summary>DISPATCH WORKFLOW W/ INPUT, IF AND NEEDS</summary>

```
---
name: Release-Golang
on:
  workflow_dispatch:
    inputs:
      release-tag:
        required: false
        type: string
  push:
    tags:
      - '*'
jobs:
  Create-Git-Tag:
    name: Release Golang
    uses: stuttgart-things/stuttgart-things/.github/workflows/git-tag.yaml@main
    if: github.ref_type != 'tag' && github.event.inputs.release-tag != ''
    with:
      tag-name: ${{ github.event.inputs.release-tag }}
      environment-name: k8s
      runs-on: arc-runner-scale-set-kaeffken
      alpine-version: 3.19.0
      continue-error: false
    secrets: inherit

  Release-Golang-Binaries:
    name: Release Golang
    uses: stuttgart-things/stuttgart-things/.github/workflows/release-golang.yaml@main
    if: always()
    needs: Create-Git-Tag
    with:
      module-name: kaeffken
      environment-name: k8s
      runs-on: arc-runner-scale-set-kaeffken
      goreleaser-version: v1.23.0
      golang-version: "1.21.5"
    secrets: inherit
```

</details>

<details><summary>WORKFLOW REPOSITORY (STORES THE WORKFLOW)</summary>

```yaml
---
name: Build & Verify Terraform Module
on:
  workflow_call:
    inputs:
      runs-on:
        required: true
        type: string
      terraform-version:
        default: 1.6
        required: true
        type: string
      tflint-version:
        default: v0.50.0
        required: true
        type: string
      environment-name:
        default: k8s
        required: true
        type: string
      continue-error:
        default: false
        required: true
        type: boolean

jobs:
  Terraform-Validate:
    runs-on: ${{ inputs.runs-on }}
    container:
      image: hashicorp/terraform:${{ inputs.terraform-version }}
    environment: ${{ inputs.environment-name }}
    continue-on-error: ${{ inputs.continue-error }}
    steps:
      - name: Checkout code
        uses: actions/checkout@v4.1.1
      - run: |
          terraform init
          terraform fmt
          terraform validate

  Terraform-Lint:
    runs-on: arc-runner-scale-set-vault-base-setup
    container:
      image: ghcr.io/terraform-linters/tflint:${{ inputs.tflint-version }}
    environment: k8s
    continue-on-error: false
    steps:
      - name: Checkout code
        uses: actions/checkout@v4.1.1
      - run: |
          tflint --recursive
```

</details>

<details><summary>CODE REPOSITORY (IMPORTS THE WORKFLOW)</summary>

```yaml
name: Terraform
on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]
  workflow_dispatch:

jobs:
  validate-terraform:
    if: github.event.ref == 'refs/heads/main'
    name: Valdiate
    uses: stuttgart-things/stuttgart-things/.github/workflows/validate-terraform.yaml@main
    with:
      environment-name: k8s
      runs-on: arc-runner-scale-set-flux2-cluster-bootstrap
      terraform-version: 1.6
      tflint-version: v0.50.0
      continue-error: false
```

</details>

<details><summary>AUTHENTICATING WITH GITHUB APP GENERATED TOKENS</summary>

- [CREATE GITHUB APP] (https://github.com/peter-evans/create-pull-request/blob/main/docs/concepts-guidelines.md#authenticating-with-github-app-generated-tokens)

  - Set GitHub App name.
  - Set Homepage URL to anything you like, such as your GitHub profile page.
  - Uncheck Active under Webhook. You do not need to enter a Webhook URL.
  - Under Repository permissions: Contents select Access: Read & write.
  - Under Repository permissions: Pull requests select Access: Read & write.
  - Under Organization permissions: Members select Access: Read-only.
  - Create a Private key from the App settings page and store it securely.

- Install the App on any repository where workflows will run requiring tokens.
- Set secrets on your repository containing the GitHub App ID, and the private key you created in step 2. e.g. APP_ID, APP_PRIVATE_KEY.
- The following example workflow shows how to use tibdex/github-app-token to generate a token for use with this action.

```yaml
steps:
  - uses: actions/checkout@v4
  - uses: tibdex/github-app-token@v1
    id: generate-token
    with:
      app_id: ${{ secrets.APP_ID }}
      private_key: ${{ secrets.APP_PRIVATE_KEY }}
  # Make changes to pull request here
  - name: Create Pull Request
    uses: peter-evans/create-pull-request@v6
    with:
      token: ${{ steps.generate-token.outputs.token }}
```

</details>

<details><summary>MULTIPLE CHOICE INPUTS (DISPATCH)</summary>

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

</details>

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

</details>

<details><summary>USE INLINE GITHUB SCRIPT FOR SETTING A GIT TAG</summary>

```yaml
name: Create-Git-Tag
on:
  workflow_dispatch:
    inputs:
      tag-name:
        required: true
        type: string

jobs:
  Create-Git-Tag:
    permissions:
      contents: write
    runs-on: arc-runner-scale-set-kaeffken
    container:
      image: alpine:3.19.0
    environment: k8s
    steps:
      - name: Create Tag
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.git.createRef({
              owner: context.repo.owner,
              repo: context.repo.repo,
              ref: 'refs/tags/v${{ inputs.tag-name }}',
              sha: context.sha
            })
```

</details>

<details><summary>DECLARE GLOBAL VARIABLES</summary>

```yaml
#..
env:
  TEMPLATE_DIR: machineShop/templates
  DESTINATION_DIR: clusters
jobs:
  #..
  steps:
    #..
    - run: |
        machineShop render \
        --source local \
        --template ${TEMPLATE_DIR}/packer-${{ inputs.os-version }}-${{ inputs.cloud }}.yaml \
        --values "provisioning=${{ inputs.ansible-provisioning }}, date=$(date '+%Y-%m-%d-%H-%M-%S'), dateShort=$(date '+%Y-%m-%d'), env=${{ inputs.env }}" \
        --output file \
        --destination ${DESTINATION_DIR}/${{ inputs.env }}/${{ inputs.cloud }}/bootstrap/packer-${{ inputs.os-version }}-${{ inputs.ansible-provisioning }}.yaml
        #..
```

</details>

<details><summary>HELMFILE ACTION</summary>

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

</details>

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

</details>

## HUGO MARKDOWN STATIC SITE GENERATOR

<details><summary>CREATE HUGO SITE</summary>

```bash
export SITE_NAME=BLOG
nerdctl run --user $(id -u):$(id -g) --rm -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine new site ${SITE_NAME} > --format yaml
```

</details>

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

</details>

<details><summary>RUN HUGO SITE</summary>

```bash
export SITE_NAME=BLOG

# EXAMPLE SITE
cp -R themes/hugo-book/exampleSite/content.en/* ./content

nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd)/blog:/src klakegg/hugo:0.107.0-ext-alpine server
```

</details>

<details><summary>BUILD STATIC CONTENT</summary>

```bash
nerdctl run --user $(id -u):$(id -g) --rm -p 1315:1313 -v $(pwd):/src klakegg/hugo:0.107.0-ext-alpine --verbose --destination public
```

</details>

<details><summary>RUN/VIEW STATIC CONTENT W/ NGINX</summary>

```bash
sudo nerdctl run -it --rm -p 8080:80 --name web -v public/:/usr/share/nginx/html nginx
```

</details>

<details><summary>YAML LINT</summary>

```bash
nerdctl run -it -v ./docs:/manifests cytopia/yamllint -- /manifests
```

</details>
