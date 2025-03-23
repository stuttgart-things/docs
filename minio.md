# stuttgart-things/docs/minio

## SNIPPETS

<details><summary><b>INSTALL MINIO-CLI (MC)</b></summary>

```bash
curl https://dl.min.io/client/mc/release/linux-amd64/mc \
  --create-dirs \
  -o $HOME/minio-binaries/mc

chmod +x $HOME/minio-binaries/mc
export PATH=$PATH:$HOME/minio-binaries/
```

</details>


<details><summary><b>USE MINIO PLAY FOR TESTING</b></summary>

```bash
mkdir -p ~/.mc/
cat << EOF> ~/.mc/config.json
{
  "version": "10",
  "aliases": {
    "play": {
      "url": "https://play.min.io",
      "accessKey": "minioadmin",
      "secretKey": "minioadmin",
      "api": "s3v4",
      "path": "auto"
    }
  }
}
EOF
```

```bash
# ZIP A TEST FOLDER (JUST FOR REFERENCE - NOT REQUIRED)
zip -r toolkit.zip toolkit/

# CREATE A BUCKET
mc mb play/ankit

# COPY TO BUCKET
mc cp toolkit.zip play/ankit
```

</details>


<details><summary><b>MC CONFIG (EXAMPLE)</b></summary>

```json
cat << EOF> ~/.mc/config.json
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
EOF
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
