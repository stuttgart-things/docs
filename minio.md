# stuttgart-things/docs/minio

## SNIPPETS

<details><summary><b>MC CONFIG (EXAMPLE)</b></summary>

```json
# cat ~/.mc/config.json
{
  "version": "10",
  "aliases": {
    "artifacts-labda": {
      "url": "https://artifacts.app.4sthings.tiab.ssc.sva.de",
      "accessKey": "<REPLACEME>",
      "secretKey": "<REPLACEME>",
      "api": "s3v4",
      "path": "auto"
    },
    "labul-automation": {
      "url": "https://artifacts.automation.sthings-vsphere.labul.sva.de",
      "accessKey": "<REPLACEME>",
      "secretKey": "<REPLACEME>",
      "api": "s3v4",
      "path": "auto"
    }
  }
}
```

</details>

<details><summary><b>MC COMMAND SNIPPETS</b></summary>

```bash
mc anonymous set public artifacts-labda/roles # SET BUCKET TO PUBLIC
mc ls artifacts-labda # LIST BUCKETS
```

</details>

## RCLONE

<details><summary>RCLONE CONFIG (EXAMPLE)</summary>

```bash
mdkir -p ${HOME}/.config/rclone/
cat <<EOF > ${HOME}/.config/rclone/rclone.conf
[labul-automation]
type = s3
provider = Minio
access_key_id = <REPLACEME>
secret_access_key = <REPLACEME>
endpoint = https://artifacts.automation.sthings-vsphere.labul.sva.de:443
acl = private
region = us-central-1
EOF
```

</details>

<details><summary>RCLONE COMMAND SNIPPETS</summary>

```bash
rclone ls labul-automation:vsphere-vm
rclone sync labul-automation:vsphere-vm . # sync bucket to current (local) dir
```

</details>
