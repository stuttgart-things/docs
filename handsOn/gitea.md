# DEPLOYMENT GITEA

## LOCAL EQUIREMENTS

```bash
apt install -y git
kubectl
helm
```

## DEPLOYMENT OF GITEA

```bash
helm upgrade --install gitea oci://registry-1.docker.io/bitnamicharts/gitea -n gitea --create-namespace
```

## CONFIGURATION GITEA

* CREATE REPO VIA WEB URL
* CREATE REPO VIA WEB GIT CLI
* CREATE PRIVATE SSH KEY
* CREATE PUBLIC SSH KEY
* CLONE
* COMMIT

## CLONE FROM GITEA (SSH)

```bash
git clone gitea@52.137.62.254:test/test2.git
```
