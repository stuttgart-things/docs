# stuttgart-things/docs/golang-k8s-operator

## INSTALL OPERATOR SDK

```bash
OPERATOR_SDK_VERSION=v1.28.1
curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${OPERATOR_SDK_VERSION}/operator-sdk_linux_amd64
sudo chmod +x operator-sdk_linux_amd64
sudo mv operator-sdk_linux_amd64 /usr/bin/operator-sdk
go version
operator-sdk version
```

## INIT/SCAFFOLD OPERATOR STRUCTURE

```bash
mkdir -p ~/projects/go/src/shipyard-operator && ~/projects/go/src/shipyard-operator
operator-sdk init \
--plugins go/v3 \
--domain sthings.tiab.ssc.sva.de \
--owner "patrick hermann" \
--project-name shipyard-operator \
--repo github.com/stuttgart-things/shipyard-operator

go mod tidy

go get sigs.k8s.io/controller-runtime@v0.14.1
```

## CREATE API/KIND

```bash
operator-sdk create api --group machineshop --version v1beta1 --kind Ansible #example
```

## EDIT TYPES

```bash
<OPERATOR-PATH>/api/<API-VERSION>/<KIND>_types.go

# EXAMPLE STRUCT SNIPPET
...
type AnsibleSpec struct {
	// +kubebuilder:default:="localhost"
	Hosts string   `json:"hosts,omitempty"`
	Vars  []string `json:"vars"`
	Roles []string `json:"roles,omitempty"`
}
...

# EXAMPLE STATUS STRUCT SNIPPET
// TERRAFORMSTATUS DEFINES THE OBSERVED STATE OF TERRAFORM
type TerraformStatus struct {
	Conditions []metav1.Condition `json:"conditions,omitempty" patchStrategy:"merge" patchMergeKey:"type" protobuf:"bytes,1,rep,name=conditions"`
}

```

## CREATE MANIFESTS

```bash
make manifests
```

## EDIT CONTROLLER

```bash
<OPERATOR-PATH>/controllers/<KIND>_controller.go

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

## CREATE CONTAINER IMAGE

```bash
nerdctl build -t <IMG-ADDRESS:IMG-TAG> . && nerdctl push <IMG-ADDRESS:IMG-TAG>
```

## DEPLOY

```bash
make deploy IMG=<IMG-ADDRESS:IMG-TAG>
```