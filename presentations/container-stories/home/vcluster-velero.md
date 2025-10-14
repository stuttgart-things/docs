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
**What are you using for Local Testing?**

> - ☁️ **Kind**
> - 🟢 **K3s**
> - 🧩 **MiniKube**
> -🪙 **Other** (please specify)**

---

> ### ❓ Audience
>
**What are you using for kubernetes secrets?**

> - ☁️ **Sops**
> - 🟢 **Vault**
> - 🧩 **Sealed Secrets**
> -🪙 **Other** (please specify)**

---

### **vCluster**

- **Lightweight, virtual clusters** that run inside a host Kubernetes cluster
- **Complete Kubernetes API** - feels like a real cluster to users
- **Shared physical infrastructure** with strong isolation
- **Perfect for multi-tenancy** and development environments

---

### **Key Benefits**
- **✅ Cost Efficiency** - Multiple clusters on shared infrastructure
- **✅ Strong Isolation** - Namespace, network, and RBAC separation
- **✅ Fast Provisioning** - Deploy in seconds vs minutes/hours
- **✅ Self-Service** - Developers can create their own clusters

---

### **Comparison: Traditional vs vCluster Approach**

| Aspect | Traditional Restricted Cluster | vCluster Approach |
|--------|-------------------------------|-------------------|
| **Developer Permissions** | Limited RBAC | Full vCluster admin |
| **Cluster Stability** | Protected by restrictions | Protected by isolation |
| **Innovation Speed** | Slow (admin approval needed) | Fast (self-service) |
| **Admin Overhead** | High (managing RBAC) | Low (automated provisioning) |
| **Security** | Rule-based restrictions | Boundary-based isolation |

---




### **Deployment Sequence**
| Step | Kustomization | Purpose | Dependencies |
|------|---------------|---------|--------------|
| **1️⃣** | `vault` | Vault secrets & ExternalSecrets | None |
| **2️⃣** | `crossplane-core` | Crossplane + ProviderConfigs | `vault` |
| **3️⃣** | `crossplane-configurations` | Restore Crossplane configurations | `crossplane-core` |
| **3️⃣** | `crossplane-configurations` | Restore Crossplane configurations | `crossplane-core` |
| **4️⃣** | `apps` | Application deployments | `crossplane-restore` |
| **5️⃣** | `backups` | Backup automation | `apps` |


{{% /section %}}
