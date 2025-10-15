+++
weight = 50
+++

{{< slide id=vcluster background-color="#9FE2BF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /VCLUSTER-VELERO

---

> ### ❓ Audience
>
**What are you using for Kubernetes Backup?**

> - ☁️ **Velero**
> - 🟢 **Kasten K10**
> - 🧩 **Custom Backup Solution**
> -🪙 **Other** (please specify)**

---

> ### ❓ Audience
>
**What are you using for K9s Testing?**

> - ☁️ **Kind**
> - 🟢 **K3s**
> - 🧩 **MiniKube**
> - 🧩 **vCluster**
> -🪙 **Other** (please specify)**

---

### **vCluster**

- **Lightweight, virtual clusters** that run inside a host Kubernetes cluster
- **Complete Kubernetes API** - feels like a real cluster to users
- **Shared physical infrastructure** with strong isolation
- **Perfect for multi-tenancy** and development environments

---

## 🚀 **vCluster Practical Use Cases**

<table style="width: 100%; background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px;">
<tr style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);">
<th style="padding: 15px; color: white; text-align: left;">Scenario</th>
<th style="padding: 15px; color: white; text-align: left;">Example</th>
</tr>
<tr>
<td style="padding: 12px; border-bottom: 1px solid #333;">Test different cluster APIs</td>
<td style="padding: 12px; border-bottom: 1px solid #333;">Run vCluster with Kubernetes 1.23 inside 1.30 host</td>
</tr>
<tr>
<td style="padding: 12px; border-bottom: 1px solid #333;">Migrate gradually</td>
<td style="padding: 12px; border-bottom: 1px solid #333;">Spin up vClusters with newer versions to test manifests</td>
</tr>
<tr>
<td style="padding: 12px; border-bottom: 1px solid #333;">CI testing</td>
<td style="padding: 12px; border-bottom: 1px solid #333;">Validate Helm charts against multiple Kubernetes versions</td>
</tr>
<tr>
<td style="padding: 12px;">Multi-version environments</td>
<td style="padding: 12px;">Each team gets preferred Kubernetes version</td>
</tr>
</table>

---

### **🛠️ Real-World Implementation**

```bash
# Create vCluster with specific Kubernetes version
vcluster create legacy-apps \
  --kubernetes-version 1.23 \
  --namespace vcluster-legacy

# Test migration to newer version
vcluster create migration-test \
  --kubernetes-version 1.28 \
  --namespace vcluster-migration

# CI/CD multi-version testing
vcluster create ci-test-1.25 --kubernetes-version 1.25
vcluster create ci-test-1.28 --kubernetes-version 1.28
vcluster create ci-test-1.30 --kubernetes-version 1.30
```

- **✅ Risk-Free Testing** - Isolated version testing
- **✅ Zero Downtime Migration** - Validate before upgrading production
- **✅ Developer Flexibility** - Teams choose their preferred versions
- **✅ Simplified CI/CD** - Test across multiple versions simultaneously

---

> ### ❓ Audience
>
**What are you using for kubernetes secrets?**

> - ☁️ **Sops**
> - 🟢 **Vault**
> - 🧩 **Sealed Secrets**
> -🪙 **Other** (please specify)**

---
## 🔄 **Flux: vCluster +Crossplane**

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/vcluster-velero.png" alt="Alt Text" width="800" style="border: 1px; box-shadow: none;" />

---

### **Deployment Sequence**
| Step | Kustomization | Purpose | Dependencies |
|------|---------------|---------|--------------|
| **1️⃣** | `vault` | Vault secrets & ExternalSecrets | None |
| **2️⃣** | `crossplane-core` | Crossplane + ProviderConfigs | `vault` |
| **3️⃣** | `crossplane-configurations` | Restore Crossplane configurations | `crossplane-core` |
| **4️⃣** | `apps` | Application deployments | `crossplane-restore` |
| **5️⃣** | `backups` | Backup automation | `apps` |

---

### **When Git Isn't Ideal for Configuration Distribution**

<table style="width: 100%; background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 15px; font-size: 0.9em;">
<tr style="background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);">
<th style="padding: 12px; color: white; text-align: left; width: 45%;">Problem with Git</th>
<th style="padding: 12px; color: white; text-align: left; width: 55%;">How OCI Solves It</th>
</tr>
<tr>
<td style="padding: 10px; border-bottom: 1px solid #333;">Git history gets large and slow with lots of YAMLs</td>
<td style="padding: 10px; border-bottom: 1px solid #333;">OCI registries handle versioned artifacts efficiently</td>
</tr>
<tr>
<td style="padding: 10px; border-bottom: 1px solid #333;">Secrets or binary manifests aren't well-suited to Git</td>
<td style="padding: 10px; border-bottom: 1px solid #333;">OCI can store and version any kind of artifact</td>
</tr>
<tr>
<td style="padding: 10px; border-bottom: 1px solid #333;">You want immutable versioning (e.g., tag v1.2.3)</td>
<td style="padding: 10px; border-bottom: 1px solid #333;">OCI tags are immutable and can be signed</td>
</tr>
<tr>
<td style="padding: 10px; border-bottom: 1px solid #333;">GitOps in air-gapped environments</td>
<td style="padding: 10px; border-bottom: 1px solid #333;">OCI registries often already approved for image hosting</td>
</tr>
<tr>
<td style="padding: 10px;">Easier promotion across environments</td>
<td style="padding: 10px;">Simple artifact promotion (dev → staging → prod)</td>
</tr>
</table>

---

### **🔄 Flux OCI Workflow**

```yaml
# Traditional Git approach
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
spec:
  url: https://github.com/org/configs
  ref:
    branch: main

# Modern OCI approach
apiVersion: source.toolkit.fluxcd.io/v1
kind: OCIRepository
spec:
  url: oci://registry.company.com/configs
  ref:
    tag: v1.5.0  # Immutable, signed version
```

### **Key Advantages of OCI for Flux**
- **✅ Efficient Storage** - No bloated Git history
- **✅ Better for Binaries** - CRDs, Helm charts, large manifests
- **✅ Immutable Releases** - Version tags never change
- **✅ Security** - Signed artifacts with Cosign
- **✅ Air-Gap Friendly** - Mirror registries instead of Git repos

{{% /section %}}
