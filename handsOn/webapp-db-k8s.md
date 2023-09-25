# WEBAPP/DB -> K8s

## CHEATSHEET

```
docker-compose up/down
kubectl get nodes
kubectl create ns
export VAR_NAME=VALUE
helm upgrade --install <RELEASE-NAME> bitnami/postgresql --version 12.12.5 --values posgres.yaml
```

## EXERCISE1: CLONE + CREATE ENV FILE

* Clone https://github.com/divrhino/divrhino-trivia-crud.git
* Create .env file (see docker-compose file) for the variables
    ```
    DB_USER=<REPLACE-WITH-YOUR-VALUE>
    DB_PASSWORD=<REPLACE-WITH-YOUR-VALUE>
    DB_NAME=<REPLACE-WITH-YOUR-VALUE>
    ```
* Export POSTGRES_USER; POSTGRES_PASSWORD; POSTGRES_DB w/ the (same) values from .env file
* Test service with docker-compose + Browser
* Stop docker compose

## EXERCISE2: CHECK KIND + DEPLOY DB W/ HELM

* Check k8s connection w/ kubectl
* Create your deployment namespace

## EXERCISE3: BUILD DOCKERIMAGE

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

* Build container image w/ docker



## EXERCISE5: CREATE SERVICE + INGRESS


* Create Service w/ kubectl in your namespace
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
---
```

Change deployment strategy
taskfile
