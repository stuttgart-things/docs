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

---

### 🧪 Example Use Case:

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/service-redis.png" alt="Alt Text" width="7000" style="border: none; box-shadow: none;" />

- Redis for tests in golang app

---




A Dagger service:

Is started as a container (like docker run)

Can expose ports (127.0.0.1:5432, for example)

Lives throughout a pipeline step or duration

Is often used for testing or integration



{{% /section %}}
