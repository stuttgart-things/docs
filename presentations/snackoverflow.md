# SnackOverflow 2027 – Vorschläge: Virtualization

Zwei Talks, die aufeinander aufbauen, aber jeweils auch einzeln funktionieren.

**Roter Faden:** Talk 1 baut die Plattform (VM → GPU-VM → Micro-VM pro CI-Job). Talk 2 nutzt sie, um KI-Agenten sicher einzusperren (Agent-VM → Micro-VM pro Agent-Session).

---

## Talk 1: Von der GPU-VM bis zur Micro-VM – Virtualisierung als Plattform-Service

### Abstract

Virtualisierung heißt längst nicht mehr nur „klassische VM“. Wir zeigen das ganze Spektrum auf einer Kubernetes-basierten Plattform: klassische VMs mit Harvester und KubeVirt, GPU-VMs mit Passthrough als Grundlage einer eigenen LLM-Plattform und Micro-VMs, die pro CI-Job in Sekunden starten und danach wieder verschwinden. Bestellt wird über Backstage, abstrahiert über Crossplane und ausgerollt per GitOps. Die Golden Images kommen aus einer Packer-Pipeline, deren Jobs selbst isoliert in Micro-VMs laufen, ohne privilegiertes Docker-in-Docker. Am Ende steht eine Plattform, die VMs, GPU-Rechenleistung und isolierte CI-Umgebungen als Self-Service anbietet. Sie ist die Basis für unseren zweiten Talk.

### Inhalte

- Rückblick: VMs as a Service mit Harvester, Crossplane und Backstage (Hack and Snack 2026)
- Golden Images als OCI-Artefakte (Packer → ORAS → Registry)
- GPU → Harvester → VM → Kubernetes: eigene LLM-Plattform
  - NVIDIA GPU Operator mit Time-Slicing
  - Ollama als Inference-Server, LiteLLM als zentrales Gateway
  - Backstage-RAG als erster Consumer
- Micro-VMs in der CI:
  - Problem: Container-Builds in CI brauchen privilegiertes Docker-in-Docker und teilen sich den Kernel
  - Lösung: GitHub Actions Runner Controller + Kata Containers (`RuntimeClass`) → jeder Job in eigener Micro-VM mit eigenem Kernel
  - Wegwerf-Umgebung pro Job, kein Zustand zwischen Builds
- Schichtenmodell und Preis der Isolation: Bare Metal → Harvester-VM → (nested) Micro-VM
- Live-Demo: VM über Backstage bestellen → Git → Crossplane → laufende VM; CI-Job startet sichtbar in eigener Micro-VM

### Technologien

#Harvester #KubeVirt #Kubernetes #RKE2 #Crossplane #KCL #Backstage #FluxCD #Packer #GitHubActions #ActionsRunnerController #ORAS #NVIDIAGPUOperator #Ollama #LiteLLM #KataContainers

---

## Talk 2: Agenten hinter Gittern – Sandboxing für KI-Coding-Agenten

### Abstract

KI-Agenten wie Claude Code, Codex oder OpenCode brauchen Shell, Netzwerk und Credentials. Aus Security-Sicht ist das ein Albtraum. Wir vergleichen die Isolationsstufen vom Container über gVisor bis zur Micro-VM, ordnen Docker Sandboxes als Referenz ein und zeigen, warum eine eigene Kernel-Grenze den Unterschied macht. Danach bauen wir es selbst und nutzen dafür die Plattform aus Talk 1: Über Backstage wird eine Agent-VM bestellt, Crossplane stellt sie auf Harvester bereit, und darin startet Docker Sandboxes pro Agent-Session eine eigene Micro-VM. Gedacht wird mit unserer eigenen LLM-Plattform. Das LLM-Gateway ist dabei der einzige erlaubte Ausgang und damit der zentrale Kontrollpunkt für Keys, Budgets und Logging. Live arbeitet ein Agent isoliert an einem Repo und liefert sein Ergebnis als Pull Request ab, sichtbar in Backstage. Der Talk funktioniert auch ohne Vorwissen aus Teil 1.

### Inhalte

- Bedrohungsmodell: Was ein autonomer Agent alles kann
- Isolationsstufen im Vergleich: Container → gVisor → Kata/Firecracker → VM
- Docker Sandboxes (Micro-VM pro Agent-Session) und Alternativen aus IT-Security-Sicht
- Eigene Sandbox-Plattform auf Basis von Talk 1:
  - **Backstage:** Template „Agent-VM“ (Repo, Aufgabe, Modell, TTL), VM und Agent-Sessions im Katalog
  - **Crossplane:** Agent-VM als Claim auf Harvester (mit Nested Virtualization)
  - **Golden Image:** Ubuntu 24.04 + `sbx` + Policy, gebaut mit Packer
  - **Docker Sandboxes:** pro Agent-Session eine Micro-VM innerhalb der Agent-VM
  - **LLM-Plattform:** GPU-Cluster als „Gehirn“, LLM-Gateway als einziger erlaubter Egress (`sbx`-Netzwerk-Policy)
- Live-Demo: Agent-VM bestellen → `sbx run` → Agent arbeitet in Micro-VM → Pull Request → Aufräumen

### Technologien

#DockerSandboxes #KataContainers #Firecracker #gVisor #Harvester #KubeVirt #Crossplane #Backstage #Packer #ClaudeCode #OpenCode #Ollama #LiteLLM #GitOps

---

## Verzahnung der Talks

| Baustein | Talk 1 | Talk 2 |
|---|---|---|
| Backstage | VM bestellen | Agent-VM bestellen, PR sichtbar |
| Crossplane | VM-/GPU-Claims | Agent-VM-Claim |
| Packer/OCI | Golden Images | Agent-VM-Image mit `sbx` |
| GPU-Cluster + LLM-Gateway | wird aufgebaut | Gehirn + Egress-Kontrollpunkt |
| Micro-VM | pro CI-Job (Kata, von der Plattform erzeugt) | pro Agent-Session (von `sbx` erzeugt) |

Talk 2 startet mit einer Folie „Unsere Plattform“ (ca. 2 Minuten), damit er auch einzeln funktioniert.

---

## Offene Punkte / To-dos

- [ ] Nested Virtualization auf dem Harvester-Host testen (`/dev/kvm` in der Guest-VM) – Voraussetzung für Kata **und** `sbx`
- [ ] `sbx` in einer Harvester-VM (Ubuntu 24.04) zum Laufen bringen
- [ ] Actions Runner Controller mit Kata-`RuntimeClass` testen (Docker-Build ohne privileged)
- [ ] GPU prüfen: RTX 5060 Ti in der 16-GB-Variante, Modellauswahl (Embedding + 7–14B Chat/Coding)
- [ ] Ollama + LiteLLM im GPU-Guest-Cluster aufsetzen
- [ ] Agent im `sbx` auf eigenes Gateway umbiegen (OpenCode einfach, Claude Code prüfen)
- [ ] `sbx`-Netzwerk-Policy: nur Git + LLM-Gateway erlauben
- [ ] Demos zusätzlich aufzeichnen (Fallback bei Live-Problemen)
- [ ] Rollenverteilung: Plattform & Demo / Security-Bewertung aufzeichnen (Fallback bei Live-Problemen)
- [ ] Rollenverteilung: Plattform & Demo / Security-Bewertung
