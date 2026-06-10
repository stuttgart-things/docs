---
layout: default
class: 'is-appendix'
num: 'F · Appendix'
meta: 'Crossplane · Composition → VM'
---

<div class="page-label">F · composition → VirtualMachine</div>

# What the claim <span class="accent">renders</span><span class="dot">.</span>

```yaml
# the HarvesterVM claim becomes a KubeVirt VirtualMachine
apiVersion: kubevirt.io/v1
kind: VirtualMachine
metadata:
  name: harvester-vm-min
  namespace: vms
  labels:
    os: ubuntu
spec:
  runStrategy: RerunOnFailure
  template:
    metadata:
      labels:
        vmName: harvester-vm-min
    spec:
      hostname: harvester-vm-min
      domain:
        cpu:
          cores: 1            # from spec.vm.cpu.cores
        resources:
          limits:
            memory: 1Gi       # from spec.vm.resources.memory
            cpu: "1"
        devices:
          disks:
            - name: rootdisk
              disk: { bus: virtio }
      volumes:
        - name: rootdisk
          persistentVolumeClaim:
            claimName: harvester-vm-min-disk
```

<p class="lede" style="margin-top: 14px; max-width: 82ch;">
The <code>create-vm</code> step turns the claim's <code>spec.vm</code> values into a full KubeVirt <code>VirtualMachine</code> — plus a PVC and cloud-init Secret from the other steps.
</p>

<style>
.slidev-code { font-size: 15px !important; line-height: 1.4 !important; padding: 20px !important; }
</style>
