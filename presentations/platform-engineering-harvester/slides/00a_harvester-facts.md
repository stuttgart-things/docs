---
layout: default
num: '00a · Harvester · KubeVirt · Key Facts'
meta: 'Harvester · KubeVirt · Rancher · HCI'
---

<div class="page-label">00a · Harvester &amp; KubeVirt — key facts</div>

# Why <span class="accent">Harvester</span><span class="dot">.</span>

<p class="lede" style="margin-top: 14px; max-width: 86ch;">
Hyperconverged infrastructure on Kubernetes — VMs as native workloads, managed like everything else in the stack.
</p>

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; margin-top: 48px;">
  <div class="surface" style="padding: 30px; min-height: 320px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">HCI</div>
      <img :src="'/logos/harvester.svg'" alt="Harvester" style="height: 32px; width: auto;" />
    </div>
    <div style="font-size: 24px; font-weight: 600; line-height: 1.2;">Hyperconverged on Kubernetes</div>
    <ul style="font-size: 17px; line-height: 1.5; margin-top: 12px; color: var(--fg-muted); padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">
      <li>Compute, storage &amp; network in <strong>one</strong> bare-metal stack — no separate SAN or vCenter.</li>
      <li>Distributed block storage via <strong>Longhorn</strong>, networking via <strong>Multus / VLAN</strong>.</li>
      <li>Built on RKE2 — <em>everything is a CRD</em>, managed with kubectl / YAML / GitOps.</li>
      <li>Open-source <strong>VMware / vSphere alternative</strong> — no per-core licensing.</li>
    </ul>
  </div>
  <div class="surface" style="padding: 30px; min-height: 320px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">ENGINE</div>
      <img :src="'/logos/kubevirt.svg'" alt="KubeVirt" style="height: 36px; width: auto;" />
    </div>
    <div style="font-size: 24px; font-weight: 600; line-height: 1.2;">KubeVirt — VMs as workloads</div>
    <ul style="font-size: 17px; line-height: 1.5; margin-top: 12px; color: var(--fg-muted); padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">
      <li>CNCF project — a VM is a <span class="mono">VirtualMachine</span> CRD.</li>
      <li><strong>VMs run inside pods</strong>: each VM lives in a <span class="mono">virt-launcher</span> pod running <strong>QEMU/KVM</strong> (libvirt).</li>
      <li>Scheduled like any pod — near-native performance via hardware virtualization.</li>
      <li>VMs &amp; containers share the cluster, network &amp; tooling (Namespaces, RBAC, NetworkPolicies).</li>
    </ul>
  </div>
  <div class="surface" style="padding: 30px; min-height: 320px;">
    <div style="display: flex; justify-content: space-between; align-items: center; min-height: 34px; margin-bottom: 14px;">
      <div class="mono" style="font-size: 14px; color: var(--accent); letter-spacing: 0.14em;">RANCHER</div>
    </div>
    <div style="font-size: 24px; font-weight: 600; line-height: 1.2;">Rancher &amp; SUSE Virtualization</div>
    <ul style="font-size: 17px; line-height: 1.5; margin-top: 12px; color: var(--fg-muted); padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">
      <li>Imported into <strong>Rancher</strong> for centralized multi-cluster management.</li>
      <li><strong>Harvester node driver</strong> provisions guest Kubernetes clusters (RKE2/K3s) — VMs as K8s worker nodes.</li>
      <li>Harvester is the upstream project; SUSE ships it commercially as <strong>SUSE Virtualization</strong>.</li>
      <li>Enterprise features: live migration, backups/snapshots, VM templates, cloud-init, GPU/PCI passthrough.</li>
    </ul>
  </div>
</div>
