# stuttgart-things/docs/certificates

## Install public cert Linux 

```bash
cd /usr/local/share/ca-certificates/
sudo update-ca-certificates
```

## Install public cert Windows

open powershell as admin

```bash
certutil -addstore "Root" "./k3s.crt"
```
