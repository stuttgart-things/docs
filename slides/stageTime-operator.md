# STAGETIME-OPERATOR
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
--
