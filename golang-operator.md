# stuttgart-things/docs/golang-operator

<details><summary>INSTALL OPERATOR SDK</summary>

```bash
OPERATOR_SDK_VERSION=v1.33.0
curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${OPERATOR_SDK_VERSION}/operator-sdk_linux_amd64
sudo chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/bin/operator-sdk
go version
operator-sdk version
```

</details>

<details><summary>INIT/SCAFFOLD OPERATOR STRUCTURE</summary>

```bash
PROJECT_NAME=stagetime-operator
DOMAIN=sthings.tiab.ssc.sva.de
GROUP=stuttgart-things
OWNER="patrick hermann"
GO_PROJECT_DIR=~/projects/golang
mkdir -p ${GO_PROJECT_DIR}/${PROJECT_NAME} && cd ${GO_PROJECT_DIR}/${PROJECT_NAME}

operator-sdk init \
--plugins go/v3 \
--domain ${DOMAIN} \
--owner ${OWNER} \
--project-name ${PROJECT_NAME} \
--repo github.com/${GROUP}/${PROJECT_NAME}

go get sigs.k8s.io/controller-runtime@v0.17.0
```

</details>

<details><summary>CREATE API KIND</summary>

```bash
operator-sdk create api --group stagetime --version v1beta1 --kind RevisionRun
make manifests
```

</details>

<details><summary>EDIT TYPES</summary>

```go
// EXAMPLE #1
//<OPERATOR-PATH>/api/<API-VERSION>/<KIND>_types.go

type AnsibleSpec struct {
	// +kubebuilder:default:="localhost"
	Hosts string   `json:"hosts,omitempty"`
	Vars  []string `json:"vars"`
	Roles []string `json:"roles,omitempty"`
}
//...
```

```go
// EXAMPLE #1
//<OPERATOR-PATH>/api/<API-VERSION>/<KIND>_types.go

type RevisionRunSpec struct {
	// INSERT ADDITIONAL SPEC FIELDS - desired state of cluster
	// Important: Run "make" to regenerate code after modifying this file
	Repository       string          `json:"repository"`
	TechnologyConfig []*Technologies `json:"technologies"`
}

type Technologies struct {
	ID   string `json:"id"`
	Kind string `json:"kind"`
	Path string `json:"path,omitempty"`
	// +kubebuilder:default=99
	Stage      int    `json:"stage,omitempty"`
	Resolver   string `json:"resolver,omitempty"`
	Params     string `json:"params,omitempty"`
	Listparams string `json:"listparams,omitempty"`
	Vclaims    string `json:"vclaims,omitempty"`
}
//...
```

```yaml
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: RevisionRun
metadata:
  labels:
    app.kubernetes.io/name: revisionrun
    app.kubernetes.io/instance: revisionrun-sample
    app.kubernetes.io/part-of: stagetime-operator
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: stagetime-operator
  name: revisionrun-sample
spec:
  repository: stuttgart-things
  technologies:
    - id: docker1
      kind: docker
      path: ./Dockerfile
      stage: 0
    - id: test
      kind: simulation
      resolver: revision=tagged
      params: scriptTimeout=10s
```


</details>

<details><summary>EXAMPLE STATUS STRUCT SNIPPET</summary>

```go
// TERRAFORMSTATUS DEFINES THE OBSERVED STATE OF TERRAFORM
type TerraformStatus struct {
	Conditions []metav1.Condition `json:"conditions,omitempty" patchStrategy:"merge" patchMergeKey:"type" protobuf:"bytes,1,rep,name=conditions"`
}
```

</details>

<details><summary>CREATE MANIFESTS</summary>

```bash
make manifests
```

</details>

<details><summary>EDIT CONTROLLER</summary>

```go
//<OPERATOR-PATH>/controllers/<KIND>_controller.go

//import(
// ..
// ctrllog "sigs.k8s.io/controller-runtime/pkg/log"
// )

# EXAMPLE CONTROLLER SNIPPET
func (r *ShipyardTerraformReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	_ = log.FromContext(ctx)

	log := ctrllog.FromContext(ctx)
	log.Info("⚡️ Event received! ⚡️")
	log.Info("Request: ", "req", req)

    // ..
	// SET STATUS
	apimeta.SetStatusCondition(&terraformCR.Status.Conditions, metav1.Condition{Type: typeAvailableTerraform,
		Status: metav1.ConditionUnknown, Reason: "Reconciling",
		Message: fmt.Sprintf(tfOperation + " operation was started for " + terraformCR.Name)})
...
}
```

</details>

<details><summary>CREATE CONTAINER IMAGE</summary>

```bash
nerdctl build -t <IMG-ADDRESS:IMG-TAG> . && nerdctl push <IMG-ADDRESS:IMG-TAG>
```

</details>

<details><summary>DEPLOY</summary>

```bash
make deploy IMG=<IMG-ADDRESS:IMG-TAG>
```

</details>

<details><summary>READ ADDITIONAL (NOT WATCHED) CRDS AS UNSTRUCTED STRUCT</summary>

```yaml
# CRD
---
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  annotations:
    controller-gen.kubebuilder.io/version: v0.11.3
  creationTimestamp: null
  name: repos.stagetime.sthings.tiab.ssc.sva.de
spec:
  group: stagetime.sthings.tiab.ssc.sva.de
  names:
    kind: Repo
    listKind: RepoList
    plural: repos
    singular: repo
  scope: Namespaced
  versions:
  - name: v1beta1
    schema:
      openAPIV3Schema:
        description: Repo is the Schema for the repos API
        properties:
          apiVersion:
            description: 'APIVersion defines the versioned schema of this representation
              of an object. Servers should convert recognized schemas to the latest
              internal value, and may reject unrecognized values. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources'
            type: string
          kind:
            description: 'Kind is a string value representing the REST resource this
              object represents. Servers may infer this from the endpoint the client
              submits requests to. Cannot be updated. In CamelCase. More info: https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds'
            type: string
          metadata:
            type: object
          spec:
            description: RepoSpec defines the desired state of Repo
            properties:
              url:
                type: string
            required:
            - url
            type: object
          status:
            description: RepoStatus defines the observed state of Repo
            type: object
        type: object
    served: true
    storage: true
    subresources:
      status: {}
```

```yaml
# EXTEND CLUSTER ROLE
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  creationTimestamp: null
  name: stagetime-operator-manager-role
rules:
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - repos
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - repos/finalizers
  verbs:
  - update
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - repos/status
  verbs:
  - get
  - patch
  - update
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - revisionruns
  verbs:
  - create
  - delete
  - get
  - list
  - patch
  - update
  - watch
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - revisionruns/finalizers
  verbs:
  - update
- apiGroups:
  - stagetime.sthings.tiab.ssc.sva.de
  resources:
  - revisionruns/status
  verbs:
  - get
  - patch
  - update
---
```

```go
// ../controllers/revisionrun_controller.go
type Repo struct {
	Url string `json:"url"`
}
//..
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

```yaml
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: Repo
metadata:
  labels:
    app.kubernetes.io/name: repo
    app.kubernetes.io/instance: repo-sample
    app.kubernetes.io/part-of: stagetime-operator
    app.kubernetes.io/managed-by: kustomize
    app.kubernetes.io/created-by: stagetime-operator
  name: repo-sample
  namespace: stagetime-operator-system
spec:
  url: https://github.com/stuttgart-things/stuttgart-things.git
```

</details>
