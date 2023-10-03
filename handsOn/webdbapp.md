# WEBAPP/DB -> K8s

## CHEATSHEET

```
docker-compose up/down
kubectl get nodes
kubectl create ns
export VAR_NAME=VALUE
helm upgrade --install <RELEASE-NAME> bitnami/postgresql --version 12.12.5 --values posgres.yaml
```
## CHEETSHEET

```
kind load docker-image webapp:<username> --name <KIND-CLUSTERNAME>
```

## EXERCISE0: PREPARATION / 'FORK' from github
* Create a git repository with the name web-app-<YOURNAME> on gitea (or init w/ git shell on your local system)
* Clone the repository to your local filesystem
* Create a README.md file in your newly created & cloned repository and push it to remote (gitea)
* Clone https://github.com/divrhino/divrhino-trivia-crud.git to your local filesystem (do not clone it inside your web-app-<YOURNAME> folder)
* Remove divrhino-trivia-crud/.git folder from the repo
* Copy everything (all files and folders) from the cloned divrhino-trivia-crud/ to web-app-<YOURNAME>
* Do not forget to copy the hidden .gitignore and .air.toml
* Push all files to your remote repo
* Remove divrhino-trivia-crud from your local filesystem
--
## EXERCISE1: TEST W/ DOCKER-COMPOSE
* Check the docker-compose.yaml file
* Verify/Add the .env file to the .gitignore file
* Create .env file (see docker-compose file) for the variables
    ```
    DB_USER=<REPLACE-WITH-YOUR-VALUE>
    DB_PASSWORD=<REPLACE-WITH-YOUR-VALUE>
    DB_NAME=<REPLACE-WITH-YOUR-VALUE>
    ```
* Export POSTGRES_USER w/ the (same) values from .env file
* Export POSTGRES_PASSWORD w/ the (same) values from .env file
* Export POSTGRES_DB w/ the (same) values from .env file
* Change the external port of the web service to something between 3001-3125
* Test service with docker-compose + Browser (172.187.248.49:<PORT>)
* Stop docker compose
* Stop docker compose
* Delete all created containers
--
## EXERCISE3: CHECK KIND + DEPLOY DB W/ HELM
* Check k8s connection w/ kubectl to the kind cluster
* Create your deployment namespace (your username)
* Deploy postgresdb w/ helm
* Check for helm values & repo https://artifacthub.io/packages/helm/bitnami/postgresql
* Create a helm values file and set values for db username; password & database + Set the value from primary.persistence.size to 1Gi
* Install the db w/ helm command in your namespace
* Check if db is running in your namespace w/ help of helm deployment output
* Check if size of db pvc is 1Gi
* push your helm values file to your git repository
--
## EXERCISE4: CHANGE HELM DEPLOYMENT INTO HELMFILE
* Create following helmfile.yaml

```
# cat Helmfile.yaml
repositories:
 - name: bitnami
   url: https://charts.bitnami.com/bitnami

releases:
- name: webserver
  namespace: web
  chart: bitnami/nginx
```

* change the release namespace
* helmfile init
* helmfile template
* helmfile apply
* check pods in namespace
* helmfile destroy
--
## EXERCISE5: UPDATE SOURCECODE & DOCKERFILE OF WEB-APP
* Update Dockerfile w/ the following content
```
FROM golang:1.19.0 as builder

WORKDIR /usr/src/app

RUN go install github.com/cosmtrek/air@latest

COPY . .

WORKDIR /usr/src/app/cmd

RUN go mod tidy && CGO_ENABLED=0 go build -buildvcs=false -o /bin/app

FROM alpine:3.17.0
COPY --from=builder /bin/app /bin/app
ADD views /web/views/
ADD public /web/public/
ENTRYPOINT ["app"]
```

* Update cmd/main.go with
```
engine := html.New("/web/views", ".html")
```
and
```
app.Static("/", "/web/public")
```
* Build the application w/ docker and the tag webapp:<username>
* Import the newly build image into kind (kind get clusters for the name of the cluster)
--
## EXERCISE5: ADD/CHANGE TASKFILE (Create a task wich builds and imports an image to your kind cluster)
* Add the file Taskfile.yaml to your app repo
* example Taskfile.yaml (copy and change)

```
---
version: 3
vars:
  DATE:
    sh: date +"%y.%m%d.%H%M"

tasks:
  build:
    desc: Builds docker image
    cmds:
      - docker build -t k8sworkshop2.azurecr.io/webapp-patrick:{{ .DATE}} .
```
* list tasks w/ task --list
* change image name to your name/image
* add task for import the image to kind:
  kind load docker-image <IMAGENAME> --name <KIND-CLUSTERNAME>
* use declared variables for it
* use task build
--
## EXERCISE6: CHANGE DB + LOGO
* Update database/database.go
```
dsn := fmt.Sprintf(
		"host=%s user=%s password=%s dbname=%s port=5432 sslmode=disable TimeZone=Asia/Shanghai",
		os.Getenv("DB_HOST"),
		os.Getenv("DB_USER"),
		os.Getenv("DB_PASSWORD"),
		os.Getenv("DB_NAME"),
)
``````
* Update the logo of the app in the static content folder and rebuild the application image w/ task:
public/divrhino-logo.png (overwrite with another png - dont change the name of the file)
---
## EXERCISE6: Deploy webapp on cluster
* Update the following deployment
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-app
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2
      maxUnavailable: 1
  selector:
    matchLabels:
      app: web-app
  replicas: 1
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
        - name: web-app
          image: webapp-patrick:23.0927.0425
          ports:
          - containerPort: 3000
          env:
          - name: DB_NAME
            value: patdb
          - name: DB_PASSWORD
            value: Atlan7is
          - name: DB_USER
            value: patrick
          - name: DB_HOST
            value: postgresql
```

```
apiVersion: v1
kind: Service
metadata:
  labels:
    app: web-app
  name: web
  namespace: default
spec:
  type: ClusterIP
  ports:
    - name: "3000"
      port: 3000
      targetPort: 3000
  selector:
    app: web-app
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: web-ingress
spec:
  rules:
  - http:
      paths:
      - pathType: ImplementationSpecific
        path: /
        backend:
          service:
            name: web
            port:
              number: 3000
```

# EXERCISE HELMFILE

```
repositories:
 - name: prometheus-community
   url: https://prometheus-community.github.io/helm-charts

releases:
- name: prom-norbac-ubuntu
  namespace: prometheus
  chart: prometheus-community/prometheus
  set:
  - name: rbac.create
    value: false
```


# ARGOCD

* go to: http://20.71.6.40
* create a new repo on gitea http://20.103.92.233 w/ the name argocd-<USERNAME>
* add a folder w/ the name pod
* add this file to the repo
```
apiVersion: v1
kind: Pod
metadata:
  name: webserver
spec:
  containers:
  - name: webserver
    image: nginx:latest
    ports:
    - containerPort: 80
```
* add your repository to argocd e.g. gitea@52.137.62.254:patrick/argocd-patrick.git
* export KUBECONFIG=~/.kube/aks
* find your created repo as a kind: Secret in the argocd namespace w/ k9s
* add the line insecure: "true"
* Create a argocd appilcation