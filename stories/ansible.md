# ANSIBLE DEV

## UPDATE ROLE -> COLLECTION

```yaml
local_requirements:
  - ansible
  - task
  - molecule (+venv & docker)
```

<details><summary>UPDATE ROLE</summary>

```bash
# clone (example!) repo and create a branch
git clone https://github.com/stuttgart-things/download-install-binary.git 
cd download-install-binary
task branch # e.g. fix/remove-unused-service-condition
# MAKE CHANGES TO CODE
```

</details>

<details><summary>TEST w/ MOLECULE</summary>

```bash
task setup-molecule
task run-molecule
```

</details>

<details><summary>UPDATE META INFORMATION + RELEASE</summary>

```bash
# ADD CHANGES, FIX OLD REFRENCES 
vi/code README.md
task commmit
```

</details>

<details><summary>RELEASE ROLE</summary>


</details>

<details><summary>UPDATE COLLECTION</summary>


</details>

<details><summary>TEST COLLECTION</summary>


</details>

<details><summary>UPDATE META INFORMATION</summary>


</details>

<details><summary>RELEASE COLLECTION</summary>


</details>
