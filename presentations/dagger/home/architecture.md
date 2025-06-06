+++
weight = 30
+++

{{< slide id=architecture background-color="#FFF5B3" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /ARCHITECTURE

---

### /DAG = Directed Acyclic Graph

```mermaid
graph TD
  A[Git Clone]
  B[Install Deps]
  C[Build]
  D[Test]
  E[Lint]
  F[Package]
  G[Publish Image]

  A --> B
  B --> C
  C --> D
  C --> E
  D --> F
  E --> F
  F --> G
```

- Directed: from one step to another
- Acyclic: No cycles — you can’t return to a previous step

---

### /Dagger

<img src="https://miro.medium.com/v2/resize:fit:1055/1*20hkHl_Jq-Olp_zU3Hpdlw.jpeg" alt="Alt Text" width="500" style="border: none; box-shadow: none;" />

- Every operation in your pipeline becomes a node in a DAG.
- Dependencies (e.g., "compile → then test") form edges between nodes.
- Dagger resolves this DAG and executes the steps efficiently — with caching.

---

### /DAGGER ENGINE

- The Dagger engine is a custom version of BuildKit
- It is responsible for efficiently running your pipeline as a DAG
- It's shipped as a container image and runs as a privileged container.

---

### /🎯 Dagger's GraphQL API spec
- You write code in Go/Python/Node using a Dagger SDK.
- That code sends GraphQL queries to a running Dagger engine (inside a container).
- The engine interprets the queries, builds the DAG of container operations, executes it, and returns results.

---

### /🎯 Why GraphQL?

- GraphQL is strongly typed and introspectable (perfect for generating SDKs).
- Lets you dynamically compose and query complex objects (like containers and filesystems).
- Supports lazy evaluation — only the final outputs you need get computed.

---

### /Example: Go SDK Query

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/go-sdk.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- Write code in a Dagger SDK
- It gets converted into a GraphQL query

---

### /Example: Go SDK Query

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/go-sdk-graph.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- The Dagger engine resolves it into a declarative build graph
- Containers run logic, results stream back via GraphQL

---

### /Cross-Language Support

<img src="https://miro.medium.com/v2/resize:fit:1400/1*gyNRqMRlB4xfm1_s0C7HXQ.png" alt="Alt Text" width="700" style="border: 1px; box-shadow: none;" />

- 🐹 Go (`github.com/dagger/dagger`)
- 🐍 Python (`dagger-io/dagger-python`)
- 🕸️ Node.js / TypeScript (`@dagger.io/dagger`)

---

### /Cross-Language Support

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/xlanguage.png" alt="Alt Text" width="5000" style="border: none; box-shadow: none;" />

- All SDKs talk to the **same GraphQL engine**
- ➡️ Language doesn't matter, pipelines behave the same
- You can reuse and compose pipeline logic across teams and stacks.

{{% /section %}}
