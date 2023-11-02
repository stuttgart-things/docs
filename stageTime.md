# stuttgart-things/docs/stageTime

## EXAMPLE PIPELINERUNS

<details open><summary>ANSIBLE-BASEOS</summary>

```yaml
---
apiVersion: tekton.dev/v1
kind: PipelineRun
metadata:
  name: execute-baseos-pve-eda-server
  namespace: tektoncd
spec:
  pipelineRef:
    resolver: git
    params:
      - name: url
        value: https://github.com/stuttgart-things/stuttgart-things.git
      - name: revision
        value: main
      - name: pathInRepo
        value: stageTime/pipelines/execute-ansible-playbooks.yaml
  workspaces:
    - name: shared-workspace
      volumeClaimTemplate:
        spec:
          storageClassName: longhorn
          accessModes:
            - ReadWriteMany
          resources:
            requests:
              storage: 1Gi
  params:
    - name: ansibleWorkingImage
      value: "eu.gcr.io/stuttgart-things/sthings-ansible:8.3.0-6"
    - name: createInventory
      value: "true"
    - name: gitRepoUrl
      value: https://github.com/stuttgart-things/stuttgart-things.git
    - name: gitRevision
      value: "main"
    - name: gitWorkspaceSubdirectory
      value: "/ansible/base-os"
    - name: vaultSecretName
      value: vault
    - name: installExtraRoles
      value: "true"
    - name: ansibleExtraRoles
      value:
        - "https://github.com/stuttgart-things/install-requirements.git"
        - "https://github.com/stuttgart-things/manage-filesystem.git"
        - "https://github.com/stuttgart-things/install-configure-vault.git"
    - name: ansiblePlaybooks
      value:
        - "ansible/playbooks/prepare-env.yaml"
        - "ansible/playbooks/base-os.yaml"
    - name: ansibleVarsFile
      value:
        - "manage_filesystem+-true"
        - "update_packages+-true"
        - "install_requirements+-true"
        - "install_motd+-true"
        - "username+-sthings"
        - "lvm_home_sizing+-'15%'"
        - "lvm_root_sizing+-'35%'"
        - "lvm_var_sizing+-'50%'"
        - "send_to_msteams+-true"
        - "reboot_all+-false"
    - name: ansibleVarsInventory
      value:
        - "all+[\"pve-eda-server.labul.sva.de\"]"
```

</details close>
