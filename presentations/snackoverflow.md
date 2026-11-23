# SnackOverflow 2027 – Vorschläge: Virtualization

Zwei Talks, die aufeinander aufbauen, aber jeweils auch einzeln funktionieren.
**Roter Faden:** Talk 1 baut die Plattform (VM → GPU-VM → Micro-VM), Talk 2 nutzt sie, um KI-Agenten sicher einzusperren.

---

## Talk 1: Von der GPU-VM bis zur Micro-VM – Virtualisierung als Plattform-Service

### Abstract

Virtualisierung heißt längst nicht mehr nur „klassische VM“. Wir zeigen das ganze Spektrum auf einer Kubernetes-basierten Plattform: klassische VMs mit Harvester und KubeVirt, GPU-VMs mit Passthrough als Grundlage einer eigenen LLM-Plattform und Micro-VMs, die in Sekunden starten und nach getaner Arbeit wieder verschwinden, zum Beispiel als isolierte CI/CD-Runner. Bestellt wird alles über Backstage, abstrahiert über Crossplane und ausgerollt per GitOps. Die Golden Images kommen aus einer Packer-Pipeline. Am Ende steht eine Plattform, die VMs, GPU-Rechenleistung und Micro-VMs als Self-Service anbietet. Sie ist die Basis für unseren zweiten Talk.

### Inhalte

- Rückblick: VMs as a Service mit Harvester, Crossplane und Backstage (Hack and Snack 2026)
- Golden Images als OCI-Artefakte (Packer → ORAS → Registry)
- GPU → Harvester → VM → Kubernetes: eigene LLM-Plattform
  - NVIDIA GPU Operator mit Time-Slicing
  - Ollama als Inference-Server, LiteLLM als zentrales Gateway
  - Backstage-RAG als erster Consumer
- Micro-VMs: Kata Containers als `RuntimeClass`, ephemere CI/CD-Runner
- Live-Demo: Bestellung über Backstage → Git → Crossplane → laufende VM

### Technologien

#Harvester #KubeVirt #Kubernetes #RKE2 #Crossplane #KCL #Backstage #FluxCD #Packer #GitHubActions #ORAS #NVIDIAGPUOperator #Ollama #LiteLLM #KataContainers #Firecracker

---

## Talk 2: Agenten hinter Gittern – Sandboxing für KI-Coding-Agenten

### Abstract

KI-Agenten wie Claude Code, Codex oder OpenCode brauchen Shell, Netzwerk und Credentials. Aus Security-Sicht ist das ein Albtraum. Wir vergleichen die Isolationsstufen vom Container über gVisor bis zur Micro-VM, ordnen Docker Sandboxes als Referenz ein und zeigen, warum eine eigene Kernel-Grenze den Unterschied macht. Danach bauen wir es selbst und nutzen dafür die Plattform aus Talk 1: Agenten-Sandboxes werden über Backstage bestellt, von Crossplane als Micro-VM bereitgestellt und nutzen unsere eigene LLM-Plattform. Das LLM-Gateway ist dabei der einzige erlaubte Ausgang und damit der zentrale Kontrollpunkt für Keys, Budgets und Logging. Live arbeitet ein Agent isoliert an einem Repo und liefert sein Ergebnis als Pull Request ab, sichtbar in Backstage. Der Talk funktioniert auch ohne Vorwissen aus Teil 1.

### Inhalte

- Bedrohungsmodell: Was ein autonomer Agent alles kann
- Isolationsstufen im Vergleich: Container → gVisor → Kata/Firecracker → VM
- Docker Sandboxes (microVM pro Agent-Session) und Alternativen aus IT-Security-Sicht
- Eigene Sandbox-Plattform auf Basis von Talk 1:
  - **Backstage:** Template „Agent-Sandbox“ (Repo, Aufgabe, Modell, TTL), Sandboxes im Katalog
  - **Crossplane:** `AgentSandbox` als weiterer Claim → Pod mit Kata-RuntimeClass (Micro-VM)
  - **Golden Image:** Sandbox-Image aus derselben Packer/OCI-Pipeline
  - **LLM-Plattform:** GPU-Cluster als „Gehirn“, Gateway als einziger Egress
- Live-Demo: Claim → Micro-VM → Agent → Pull Request → Sandbox wird abgeräumt

### Technologien

#DockerSandboxes #KataContainers #Firecracker #gVisor #KubeVirt #Crossplane #Backstage #ClaudeCode #OpenCode #Ollama #LiteLLM #NetworkPolicies #GitOps

---

## Verzahnung der Talks

| Baustein | Talk 1 | Talk 2 |
|---|---|---|
| Backstage | VM bestellen | Agent-Sandbox bestellen, PR sichtbar |
| Crossplane | VM-/GPU-Claims | `AgentSandbox`-Claim |
| Packer/OCI | Golden Images | Sandbox-Image |
| GPU-Cluster + LLM-Gateway | wird aufgebaut | Gehirn + Egress-Kontrollpunkt |
| Micro-VM (Kata) | CI/CD-Runner | Isolation der Agenten |

Talk 2 startet mit einer Folie „Unsere Plattform“ (ca. 2 Minuten), damit er auch einzeln funktioniert.

---

## Offene Punkte / To-dos

- [ ] Nested Virtualization auf dem Harvester-Host testen (`/dev/kvm` in der Guest-VM für Kata)
- [ ] GPU prüfen: RTX 5060 Ti in der 16-GB-Variante, Modellauswahl (Embedding + 7–14B Chat/Coding)
- [ ] Ollama + LiteLLM im GPU-Guest-Cluster aufsetzen
- [ ] Agent mit lokalem Modell testen (OpenCode), Cloud-Modell als Vergleich/Fallback
- [ ] Demos zusätzlich aufzeichnen (Fallback bei Live-Problemen)
- [ ] Rollenverteilung: Plattform & Demo / Security-Bewertung
