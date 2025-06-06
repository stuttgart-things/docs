+++
weight = 70
+++

{{< slide id=up background-color="#D4B9FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /SERVICE

---

### /What Is a Dagger Service?

- A **background container** used in builds
- Exposes ports for use during a pipeline
- Lives only for the duration of the pipeline step
- Can expose ports (127.0.0.1:5432, for example)
- Lives throughout a pipeline step or duration
- Is often used for testing or integration

---

### 🧪 Example Use Case

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/service-redis.png" alt="Alt Text" width="1000" style="border: none; box-shadow: none;" />

- Redis for tests in golang app

---

### 🧪 /MORE DETAILED

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/test.png" alt="Alt Text" width="1000" style="border: none; box-shadow: none;" />

- Build golang bin
- Run go test
- Run test w/ build binary

---

### 🧪 /ANOTHER ONE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/serve.png" alt="Alt Text" width="1000" style="border: none; box-shadow: none;" />



{{% /section %}}
