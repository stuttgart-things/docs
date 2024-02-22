# MAKING OF stageTime


<span style="color:orange">HACK & SNACK 2024</span>

<!-- .slide: data-transition="zoom" -->
--
### /INTRO

<span style="color:yellow">#DevOps #CICD #Automation #Cloud #IAC #Kubernetes #Containerization</span> <br><br>
<!-- .element: class="fragment fade-up" -->

Patrick Hermann <!-- .element: class="fragment fade-up" -->
System-Engineer (Stuttgart) <!-- .element: class="fragment fade-up" -->
patrick.hermann@sva.de <!-- .element: class="fragment fade-up" -->
<!-- .element: class="fragment fade-up" -->
--
# /AGENDA
--
### /CHAPTER1: CHALLENGE
* INTRO <!-- .element: class="fragment fade-up" -->
* PIPELINE AS CODE ON KUBERETES <!-- .element: class="fragment fade-up" -->
* TEKTON <!-- .element: class="fragment fade-up" -->
* CHALLENGES <!-- .element: class="fragment fade-up" -->
--
### /CHAPTER2: SERVER
* SERVICE <!-- .element: class="fragment fade-up" -->
* GOLANG <!-- .element: class="fragment fade-up" -->
* GRPC <!-- .element: class="fragment fade-up" -->
* VCLUSTER <!-- .element: class="fragment fade-up" -->
--
### /CHAPTER3: CREATOR
* SERVICE <!-- .element: class="fragment fade-up" -->
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* TASKFILE <!-- .element: class="fragment fade-up" -->
--
### /CHAPTER4: INFORMER
* SERVICE <!-- .element: class="fragment fade-up" -->
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* HELMTEST <!-- .element: class="fragment fade-up" -->
* INFORMER <!-- .element: class="fragment fade-up" -->
--
### /CHAPTER5: OPERATOR
* SERVICE <!-- .element: class="fragment fade-up" -->
* FEATURES <!-- .element: class="fragment fade-up" -->
* DYNAMIC KUBERNETES W/ GOLANG <!-- .element: class="fragment fade-up" -->
* HELMFILE <!-- .element: class="fragment fade-up" -->
---
# /STAGETIME-INTRO
--
### /CI-CD TASKS
* Lint: to keep our code clean and maintainable <!-- .element: class="fragment fade-up" -->
* Build: put all of our code together into runnable software bundle <!-- .element: class="fragment fade-up" -->
* Test: to ensure we don't break existing features <!-- .element: class="fragment fade-up" -->
* Package: Put it all together as build artifacts <!-- .element: class="fragment fade-up" -->
--
### /PIPELINES AS CODE
* Can be audited for changes just like any other files in the repository <!-- .element: class="fragment fade-up" -->
* Codify build, test + deploy process for code <!-- .element: class="fragment fade-up" -->
* empower teams to create standard processes across multiple repositories <!-- .element: class="fragment fade-up" -->
--
### /PIPELINES AS CODE ON K8S
* CUSTOMIZABLE <!-- .element: class="fragment fade-up" -->
* REUSABLE<!-- .element: class="fragment fade-up" -->
* SCALABLE <!-- .element: class="fragment fade-up" -->
* STANDARDIZED <!-- .element: class="fragment fade-up" -->
--
### /TEKTON-PIPELINES
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/tekton-horizontal-color.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Tekton Pipelines is a Kubernetes extension <!-- .element: class="fragment fade-up" -->
* Runs on every Kubernetes cluster <!-- .element: class="fragment fade-up" -->
* Defines a set of Custom Resources that act as building blocks <!-- .element: class="fragment fade-up" -->
--
### /TASK
* Defines a series of steps <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: Task
metadata:
  name: git-clone
spec:
  steps:
    - name: clone-git
      image: gcr.io/git-init:v0.40.2
      script: |
        #!/bin/sh
        echo "Cloning git repository"
        # ..
```
<!-- .element: class="fragment fade-up" -->
--
### /Pipeline
* Series of Tasks that accomplish a specific build goal  <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: Pipeline
metadata:
  name: clone-build-push
spec:
  params:
  - name: repo-url
    type: string
  workspaces:
  - name: shared-data
  tasks:
  - name: fetch-source
    taskRef:
      name: git-clone
```
<!-- .element: class="fragment fade-up" -->
--
### /PipelineRun
* Instantiates a Pipeline for execution with specific inputs, outputs, and execution parameters  <!-- .element: class="fragment fade-up" -->

```
apiVersion: tekton.dev/v1beta1
kind: PipelineRun
metadata:
  generateName: clone-build-push-run-
spec:
  pipelineRef:
    name: clone-build-push
  params:
  - name: repo-url
    value: https://github.com/google/docsy-example.git
  workspaces:
  - name: shared-data
  # ..
```
<!-- .element: class="fragment fade-up" -->
--
### /LIST PIPELINERUNS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prlist.gif" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /PIPELINERUN LOGS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prlogs.gif" width="1000"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /STARTING POSITION
* PIPELINES AS MICROSERVICES <!-- .element: class="fragment fade-up" -->
* RUN PIPELINERUNS IN STAGES <!-- .element: class="fragment fade-up" -->
    * PARALLEL (=SAME STAGE) <!-- .element: class="fragment fade-up" -->
    * RUN OF A SEQUENCE OF STAGES <!-- .element: class="fragment fade-up" -->
--
### /STARTING POSITION
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/stages.png" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /STAGETIME
* BEGININGS IN 2022 <!-- .element: class="fragment fade-up" -->
* TEAM SÜD-WEST <!-- .element: class="fragment fade-up" -->
--
### /DESIGN PRINCIPLES TEKTON PIPELINES/RUNS
* PIPELINE AS MICROSERVICES <!-- .element: class="fragment fade-up" -->
* RESOLVER (GIT) <!-- .element: class="fragment fade-up" -->
* CSI DRIVER (SECRETS) <!-- .element: class="fragment fade-up" -->
* VOLUMEN CLAIM TEMPLATES (K8S) <!-- .element: class="fragment fade-up" -->
--
### /GOALS STAGETIME
* EVENT-DRIVEN PIPELINERUNS (BY COMMIT/REVISION) <!-- .element: class="fragment fade-up" -->
* PARALLEL/DEPENDET RUNS <!-- .element: class="fragment fade-up" -->
* STANDARDIZED BUILDING BLOCKS OF CI/CD <!-- .element: class="fragment fade-up" -->
* HOUSEKEEPING TEKTON PIPELINERUNS/PODS/PVCS <!-- .element: class="fragment fade-up" -->
---
# /STAGETIME-SERVER
--
### /GOLANG
[<img src="https://miro.medium.com/v2/resize:fit:2000/1*8bPiDNL1K1ZdK9O_T5IVKw.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Same language in which Kubernetes is built <!-- .element: class="fragment fade-up" -->
* Most natural fit for Kubernetes extensions, custom controls and operators <!-- .element: class="fragment fade-up" -->
--
### /REST
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/rest.png" width="1000"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /GRPC
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/grpc.png" width="1000"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /PROTO DEFINITION
```
syntax = "proto3";

package revisionrun;

import "revisionrun/pipelinerun.proto";

message CreateRevisionRunRequest {
    string repo_name = 1;
    string pushed_at = 2;
    string author = 3;
    string repo_url = 4;
    string commit_id = 5;
    repeated Pipelinerun pipelineruns = 6;
}
```
<!-- .element: class="fragment fade-up" -->
--
### /COMPILE-GENERATE FOR GOLANG
```
protoc --go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
revisionrun/*.proto
```
<!-- .element: class="fragment fade-up" -->
--
### /GENERATED CODE
```
//..
func (x *CreateRevisionRunRequest) ProtoReflect()
protoreflect.Message {
	mi := &file_revisionrun_revisionrun_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms :=
		protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}
```
<!-- .element: class="fragment fade-up" -->
--
### /SERVER

```
listener, err := net.Listen("tcp", "0.0.0.0"+serverPort)
if err != nil {
	log.Fatalln(err)
}
grpcServer := grpc.NewServer()
reflection.Register(grpcServer)
registerServices(grpcServer)

func registerServices(s *grpc.Server) {
	revisionrun.RegisterStageTimeApplicationServiceServer
	(s, &Server{})
	revisionrun.RegisterStatusesServer
	(s, &StatusService{})
}
```
<!-- .element: class="fragment fade-up" -->
--
### /CLIENT

```
//..
conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))

if err != nil {
  fmt.Println(err)
}
defer conn.Close()

stsClient := NewClient(conn, time.Second)
err = stsClient.CreateRevisionRun(context.Background(),
bytes.NewBuffer(revisionRunJson))
//..
```
<!-- .element: class="fragment fade-up" -->
--
### /INPUT-FILE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prsjson.png" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /SEQUENCE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/server.png" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
# /TASKFILE
--
### /What is Taskfile?
[<img src="https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png" width="700"/>](https://www.sva.de/index.html)
--
### /What is Taskfile?
*  tool designed to make executing terminal commands or even lists of commands needed for specific operations easier <!-- .element: class="fragment fade-up" -->
* Task is a tool written in Golang <!-- .element: class="fragment fade-up" -->
* The syntax is based on YAML, which requires a specific structure <!-- .element: class="fragment fade-up" -->
* It's a much simpler solution compared to GNU make <!-- .element: class="fragment fade-up" -->
* Getting started with Taskfile is very easy <!-- .element: class="fragment fade-up" -->
--
### /Taskfile Example

```
version: 3
tasks:
  build:
    desc: Build the app
    deps: [lint, proto]
    cmds:
      - go mod tidy
      - CGO_ENABLED=0
      - GOOS=linux
      - go install \
        -ldflags="-X {{ .MODULE }}/internal.date={{ .DATE }} \
        -X {{ .MODULE }}/internal.commit={{ .GIT_COMMIT }}"
```
---
# /STAGETIME-CREATOR
--
### /SERVICE
* POLLS REDIS FOR TASKS/RESOURCES TO CREATE (STREAMS) <!-- .element: class="fragment fade-up" -->
* READS PIPELINERUNS FROM REDIS (JSON) <!-- .element: class="fragment fade-up" -->
* CREATES PIPELINERUNS ON CLUSTER <!-- .element: class="fragment fade-up" -->
--
### /REDIS-STREAMS
* Event sourcing with Redis Streams and Go <!-- .element: class="fragment fade-up" -->
* stageTime-Server: publisher <!-- .element: class="fragment fade-up" -->
* stageTime-creator: consumers <!-- .element: class="fragment fade-up" -->
--
### /SEQUENCE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/creator.png" width="1500"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /RESOURCE CREATION
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/creator.gif" width="1500"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /LIST CREATED PIPELINERUNS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/prlistcreator.gif" width="1500"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /HELM
* A helm chart is just a template for creating and deploying applications on Kubernetes using Helm <!-- .element: class="fragment fade-up" -->
[<center><img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F415d986e-939a-4773-a022-e7d42296e1eb_380x222.png" width="750"/></center>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /HELM
* Helm is a package manager for Kubernetes applications that includes templating and lifecycle management functionality <!-- .element: class="fragment fade-up" -->
[<img src="https://substackcdn.com/image/fetch/f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6cf41a23-e1cb-41cb-b53a-0e706baf9a76_562x212.png" width="1500"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /HELM CHART.YAML

```
apiVersion: v2
name: stagetime-creator
description: Helm chart for Kubernetes
type: application
version: v0.1.100
appVersion: v0.1.100
dependencies:
  - name: sthings-helm-toolkit
    version: 2.4.58
    repository: oci://eu.gcr.io/stuttgart-things
```
<!-- .element: class="fragment fade-up" -->
--
### /TEMPLATE - DEFINITION
```
{{- define "sthings-helm-toolkit.deployment" -}}
{{- $envVar := first . -}}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ $envVar.Values.deployment.name | default (include "sthings-helm-toolkit.fullname" . )}}
  annotations:
  {{- range $key, $value := $envVar.Values.deployment.annotations }}
    {{ $key }}: {{ $value | quote }}
  {{- end }}{{- end }}
```
<!-- .element: class="fragment fade-up" -->
--
### /TEMPLATE - INCLUDE
```
{{- $envVar := . -}}
{{ include "sthings-helm-toolkit.deployment" (list $envVar) }}
```
<!-- .element: class="fragment fade-up" -->
--
### /HELM VALUES
```
deployment:
  name: stagetime-creator
  volumes:
    manifest-templates:
      volumeKind: configMap
  labels:
    app: stagetime-creator
  selectorLabels:
    app: stagetime-creator
  allowPrivilegeEscalation: "false"
  privileged: "false"
  runAsNonRoot: "false"
```
<!-- .element: class="fragment fade-up" -->
---
# /STAGETIME-INFORMER
--
### /SERVICE
* INFORMS ABOUT PIPELINERUN EVENTS: <!-- .element: class="fragment fade-up" --> <span style="color:orange">ADD, UPDATE & DELETE</span>
* STORES RESULTS (SUCCESSFUL/FAILED STAGES) IN REDIS (JSON) <!-- .element: class="fragment fade-up" -->
* TRIGGERS NEW STAGE(-RUNS) (STREAMS) <!-- .element: class="fragment fade-up" -->
--
### /INFORMING KINDS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-kinds.png" width="1800"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /INFORMER CODE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-code.png" width="800"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /INFORMER LOGS
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer-logs.png" width="2000"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /SEQUENCE
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/informer.png" width="1500"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /HELMFILE
* Compose several charts together to create a comprehensive deployment artifact <!-- .element: class="fragment fade-up" -->
* Separating Environment specific information from charts <!-- .element: class="fragment fade-up" -->
* Helmfile templates helm templates <!-- .element: class="fragment fade-up" -->
--
### /HELMFILE RELEASES
* DEFINE MULTIPLE RELEASES <!-- .element: class="fragment fade-up" -->

```
releases:
  - name: redis-stack
    installed: false
    namespace: stagetime-informer-redis
    chart: redis/redis
    version: 17.1.4
    values:
      - "env/redis-stack.yaml.gotmpl"
  - name: stagetime-informer
    installed: true
    # ...
```
<!-- .element: class="fragment fade-up" -->
--
### /HELMFILE ENVIRONMENTS
```
environments:
  labul-pve-dev:
    values:
      - env/defaults.yaml
      - env/{{ .Environment.Name }}.yaml
  vcluster:
    values:
      - env/defaults.yaml
      - env/{{ .Environment.Name }}.yaml
```
<!-- .element: class="fragment fade-up" -->
--
### /HELM VALUES
```
namespace: {{ .Release.Namespace }}
secrets:
  redis-connection:
    name: redis-connection
    labels:
      app: stagetime-server
    dataType: stringData
    secretKVs:
      REDIS_SERVER: {{ .Values.redisStack.serviceName }}
      REDIS_PORT: {{ .Values.redisStack.port }}
      REDIS_PASSWORD: {{ .Values.redisStack.password }}
```
<!-- .element: class="fragment fade-up" -->
--
### / HELMFILE VALUES
```
ingressDomain: cd43.sthings-pve.labul.sva.de
redisPassword: ref+vault://stagetime/redis/password
redisServer: redis-stack-headless.\
stagetime-redis.svc.cluster.local
```
<!-- .element: class="fragment fade-up" -->
---
# /STAGETIME-OPERATOR
--
### /SERVICE
* WATCHES KIND REVISIONRUN <!-- .element: class="fragment fade-up" -->
* READS CRS KIND REPO + PIPELINERUNTEMPLATE <!-- .element: class="fragment fade-up" -->
* TRIGGERS STAGETIME SERVER <!-- .element: class="fragment fade-up" -->
* STATUS FOR REVISIONRUN <!-- .element: class="fragment fade-up" -->
--
### /OPERTOR-FRAMWORK
* PROJECT INIT <!-- .element: class="fragment fade-up" -->
* DEFINE TYPES <!-- .element: class="fragment fade-up" -->
* GENERATE CRDS + MANIFESTS <!-- .element: class="fragment fade-up" -->
* EDIT CONTROLLER <!-- .element: class="fragment fade-up" -->
* BUILD IMAGE <!-- .element: class="fragment fade-up" -->
* DEPLOY <!-- .element: class="fragment fade-up" -->
* CREATE CUSTOM RESOURCE <!-- .element: class="fragment fade-up" -->
--
### /PROJECT INIT
```
GO_PROJECT_DIR=~/projects/golang
mkdir -p ${GO_PROJECT_DIR}/${PROJECT_NAME} \
&& cd ${GO_PROJECT_DIR}/${PROJECT_NAME}

operator-sdk init \
--plugins go/v3 \
--domain ${DOMAIN} \
--owner ${OWNER} \
--project-name ${PROJECT_NAME} \
--repo github.com/${GROUP}/${PROJECT_NAME}
```
<!-- .element: class="fragment fade-up" -->
--
### /DEFINE TYPES
```
type RevisionRunSpec struct {
	Repository       string          `json:"repository"`
	TechnologyConfig []*Technologies `json:"technologies"`
}

type Technologies struct {
	ID   string `json:"id"`
	Path string `json:"path,omitempty"`
	// +kubebuilder:default=99
	Stage      int    `json:"stage,omitempty"`
	Resolver   string `json:"resolver,omitempty"`
	Params     string `json:"params,omitempty"`
	Listparams string `json:"listparams,omitempty"`
}
```
<!-- .element: class="fragment fade-up" -->
--
### /EDIT CONTROLLER
```
func (r *RevisionRunReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	_ = log.FromContext(ctx)

	log := ctrllog.FromContext(ctx)
	log.Info("⚡️ Event received! ⚡️")
	log.Info("Request: ", "req", req)

	// GET REVISION RUN
	revisionRun := &stagetimev1beta1.RevisionRun{}
	// ..
```
<!-- .element: class="fragment fade-up" -->
--
### /REVISIONRUN-CR
```
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: RevisionRun
metadata:
  name: revisionrun-simulation
spec:
  repository: stuttgart-things
  #revision: ad3121246532123
  technologies:
    - id: image-build
      kind: docker
      resolver: revision=main
      params: scriptTimeout=10s
      canfail: false
```
<!-- .element: class="fragment fade-up" -->
--
### /UNSTRUCTURED STRUCT
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/twitter-unstructred.png" width="700"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
### /UNSTRUCTURED STRUCT
* You need to work with Kubernetes Objects in a generic way? <!-- .element: class="fragment fade-up" -->
* You don't want to or cannot depend on the api module? <!-- .element: class="fragment fade-up" -->
* You need to work with Custom Resources that aren't defined in the api module? <!-- .element: class="fragment fade-up" -->
--
### /KIND REPOSITORY
```
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: Repo
metadata:
  name: stuttgart-things
spec:
  name: stuttgart-things
  organization: stuttgart-things
  branch: main
```
<!-- .element: class="fragment fade-up" -->
--
### /GET UnstructuredContent FROM CR
```
u := &unstructured.Unstructured{}
u.SetGroupVersionKind(schema.GroupVersionKind{
	Group:   "stagetime.sthings.tiab.ssc.sva.de",
	Kind:    "Repo",
	Version: "v1beta1",
})

_ = r.Client.Get(context.Background(), client.ObjectKey{
	Name:      "repo-sample",
	Namespace: "stagetime-operator-system",
}, u)

spec := u.UnstructuredContent()["spec"]

repo := Repo{}
dbByte, _ := json.Marshal(spec)
_ = json.Unmarshal(dbByte, &repo)

fmt.Println(repo.Url)
```
<!-- .element: class="fragment fade-up" -->
---
# /OUTRO
--
### /LEARNINGS (SO FAR)
* gRPC SERVICE (MULTIPLE+COMPLEX JSON)<!-- .element: class="fragment fade-up" -->
* KUBERNETES GOLANG DYNAMIC CLIENT<!-- .element: class="fragment fade-up" -->
* REDIS STACK: STREAMS, JSON<!-- .element: class="fragment fade-up" -->
* KUBERNETES OPERATOR + NOT WATCHED CRS<!-- .element: class="fragment fade-up" -->
--
### /COMING UP SERVICES
* stageTime-analyzer<!-- .element: class="fragment fade-up" -->
* stageTime-fetcher<!-- .element: class="fragment fade-up" -->
* stageTime-scheduler<!-- .element: class="fragment fade-up" -->
--
### /COMING UP TOPICS
* INTEGRATION W/ ARGOCD PULL REQUEST GENEARTOR + GITHUB API<!-- .element: class="fragment fade-up" -->
* STANDARDIZED TEKTON CATALOG AS OCI/GIT BUNDLES<!-- .element: class="fragment fade-up" -->
--
### /TRIVIA
* tbd<!-- .element: class="fragment fade-up" -->
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/sthings-train.png" width="600"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
