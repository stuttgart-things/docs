# /KUSTOMIZE
--
### /OVERVIEW
* Kustomize is a configuration customization tool for Kubernetes clusters <!-- .element: class="fragment fade-up" -->
* It allows administrators to make declarative changes using untemplated files, leaving original manifests untouched <!-- .element: class="fragment fade-up" -->
* All customization specifications are contained within a kustomization.yaml file, which superimposes specifications on top of existing manifests to generate custom versions of resources <!-- .element: class="fragment fade-up" -->
--
### /USECASE
* With kustomize, your team can ingest any base file updates for your underlying components while keeping use-case specific customization overrides intact <!-- .element: class="fragment fade-up" -->
* Another benefit of utilizing patch overlays is that they add dimensionality to your configuration settings, which can be isolated for troubleshooting misconfigurations or layered to create a framework of most-broad to most-specific configuration specifications <!-- .element: class="fragment fade-up" -->
--
### /reusability
* Base Layer -> Specifies the most common resources <!-- .element: class="fragment fade-up" -->
* Patch Layers -> Specifies use case specific resources <!-- .element: class="fragment fade-up" -->
--
### /Benefits of Using Kustomize
* Reusability <!-- .element: class="fragment fade-up" -->
    * Kustomize allows you to reuse one base file across all of your environments (development, staging, production) and then overlay unique specifications for each <!-- .element: class="fragment fade-up" -->

* Fast Generation <!-- .element: class="fragment fade-up" -->
    * Since Kustomize has no templating language, you can use standard YAML to quickly declare your configurations <!-- .element: class="fragment fade-up" -->

* Easier to Debug <!-- .element: class="fragment fade-up" -->
    * YAML itself is easy to understand and debug when things go wrong <!-- .element: class="fragment fade-up" -->
    * Pair that with the fact that your configurations are isolated in patches, and you’ll be able to triangulate the root cause of performance issues in no time <!-- .element: class="fragment fade-up" -->
    * Simply compare performance to your base configuration and any other variations that are running <!-- .element: class="fragment fade-up" -->
--
### /Kustomise project structure
* A Kustomize project structure typically comprises a base and overlays directory <!-- .element: class="fragment fade-up" -->
* In our sample specification above, the base directory contains a file named kustomization.yaml and manifest files for shared resources <!-- .element: class="fragment fade-up" -->
* The base/kustomization.yaml file declares the resources that Kustomize will include in all environments, while the shared manifest files define specific configurations for these resources <!-- .element: class="fragment fade-up" -->
--
### /Kustomise project structure
└── base
│   ├── shared-manifest-file-1.yaml
│   ├── kustomization.yaml
│   └── shared-manifest-file-2.yaml
└── overlays
    ├── env-1
    │   ├── unique-manifest-file-1.yaml
    │   └── kustomization.yaml
    ├── env-2
    │   ├── unique-manifest-file1.yaml
    │   ├── kustomization.yaml
    │   ├── unique-manifest-file2.yaml
    │   └── unique-manifest-file3.yaml
    └── env-3
        ├── unique-manifest-file1.yaml
        ├── kustomization.yaml
        └── unique-manifest-file3.yaml
--
### /Kustomise project structure
* The overlays directories include customization files (also named kustomization.yaml) that reference configurations within the shared manifests of the base folder and apply defined patches to build custom resources <!-- .element: class="fragment fade-up" -->
* The overlays directory also includes individual manifest files, which Kustomize uses to create resources specific to the environment where the files reside <!-- .element: class="fragment fade-up" -->
--
## Kustomize vs Helm
|                            | Kustomize   | Helm       |
|----------------------------|-------------|------------|
| Method of operation        | overlays    | templating |
| Ease of use                | simple      | complex    |
| Support for packaging      | no          | yes        |
| Native kubectl integration | yes         | no         |
| Declarative/ imperative    | declarative | imperative |

--
## Demo: change image names and tags


--
https://github.com/kubernetes-sigs/kustomize/blob/master/examples/image.md
https://github.com/CariZa/kustomize-practice
https://levelup.gitconnected.com/kubernetes-change-base-yaml-config-for-different-environments-prod-test-6224bfb6cdd6