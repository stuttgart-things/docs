# /GIT

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

## GITCONFIG

<details open><summary><b>EXAMPLE CONFIG #1</b></summary>

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

