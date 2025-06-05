+++
weight = 25
+++

{{< slide id=shell background-color="#FFA2A2" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# DAGGER SHELL

---

### CALL FUNCTION

```bash
dagger -m github.com/stuttgart-things/dagger/docker@v0.9.0
.help trivy-scan
trivy-scan nginx:latest
```

---

### EXECUTE CONTAINER #1

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/shell_golang.gif" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- install package(s) into container

---

### EXECUTE CONTAINER #2


---

### EXECUTE CONTAINER #3


---

### EXECUTE CONTAINER #4

---







## DAGGER SHELL - JUMP INTO CONTAINER

```bash
container |
  from alpine |
  with-exec apk add git |
  terminal
```

## DAGGER SHELL - SIMPLE CONTAINER BUILD

```bash


```


{{% /section %}}
