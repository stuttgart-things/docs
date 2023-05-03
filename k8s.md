# K8S

## NAMESPACE STUCK IN DELETION

#### OPTION1: DELETE PENDING APISERVICES
```
kubectl get apiservice|grep False
kubectl delete APIServices v1alpha1.apps.kio.kasten.io # example
```

#### OPTIONW: CHANGE FINALIZER
```
kubectl get namespace "<NAMESPACE>" -o json \
  | tr -d "\n" | sed "s/\"finalizers\": \[[^]]\+\]/\"finalizers\": []/" \
  | kubectl replace --raw /api/v1/namespaces/<NAMESPACE>/finalize -f -
```
