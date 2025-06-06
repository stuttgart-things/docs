+++
weight = 25
+++

{{< slide id=shell background-color="#FFA2A2" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# DAGGER SHELL

---

### /DAGGER SHELL

- The Dagger CLI includes an interactive shell
- translates the familiar Bash syntax to Dagger API requests
- simplest and fastest way to run Dagger workflows directly from the command-line.

---

### /EXECUTE CONTAINER FROM SHELL

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/shell_golang.gif" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- install package(s)

---

### /BUILD GO BINARY

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/build.png" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- Clone git repo
- Build binary
- Export binary to dir

---

### /VARIABLES + TERMINAL EXAMPLE

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/shell_node_nginx.gif" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- Set vars
- Get Interactive terminal

---

### /USE FROM BASH (OR SCRIPT)

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/script.png" alt="Alt Text" width="1700" style="border: none; box-shadow: none;" />

---

### /FUNCTION, CONTAINER BUILD + PUBLISH

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/shell_node_publish2.gif" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

---

> ### ❓ Audience
>
> **HOW DO YOU BUILD CONTAINER IMAGES? **
>
> - 🐳 Docker
> - 🔥 Kaniko
> - 🌱 Buildah
> - 🦀 Ko
> - 🐺 Apko
> - ..?


---

### /COMPOSING CONTAINER BUILD

<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/dagger/composing.png" alt="Alt Text" width="800" style="border: none; box-shadow: none;" />

- loads github.com/dagger/dagger/docs into one pipeline
- github.com/dagger/dagger/modules/wolfi into another
- then combines them.


{{% /section %}}
