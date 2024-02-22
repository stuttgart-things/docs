# STAGETIME-OPERATOR
--
## SERVICE
* WATCHES KIND REVISIONRUN <!-- .element: class="fragment fade-up" -->
* READS KIND REPO + PIPELINERUNTEMPLATE <!-- .element: class="fragment fade-up" -->
* TRIGGERS STAGETIME SERVER <!-- .element: class="fragment fade-up" -->
* STATUS FOR REVISIONRUN <!-- .element: class="fragment fade-up" -->
--
## REVISIONRUN-CR

```
apiVersion: stagetime.sthings.tiab.ssc.sva.de/v1beta1
kind: RevisionRun
metadata:
  labels:
    app.kubernetes.io/name: revisionrun
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
--
## OPERTOR-FRAMWORK
* PROJECT INIT <!-- .element: class="fragment fade-up" -->
* DEFINE TYPES <!-- .element: class="fragment fade-up" -->
*  <!-- .element: class="fragment fade-up" -->

--
## OPERTOR-FRAMWORK

## PROJECT INIT

```
GO_PROJECT_DIR=~/projects/golang
mkdir -p ${GO_PROJECT_DIR}/${PROJECT_NAME} && cd ${GO_PROJECT_DIR}/${PROJECT_NAME}

operator-sdk init \
--plugins go/v3 \
--domain ${DOMAIN} \
--owner ${OWNER} \
--project-name ${PROJECT_NAME} \
--repo github.com/${GROUP}/${PROJECT_NAME}
```
<!-- .element: class="fragment fade-up" -->
--
## EDIT TYPES

```
type RevisionRunSpec struct {
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
```
<!-- .element: class="fragment fade-up" -->
--
## EDIT TYPES
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